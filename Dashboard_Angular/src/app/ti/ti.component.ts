import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { ApiService } from '../api/api.service';
import { Component, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { BreakpointObserver, Breakpoints, BreakpointState } from '@angular/cdk/layout';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Icons } from 'ng-bootstrap-icons/bootstrap-icons/icons.provider';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatPaginator } from '@angular/material/paginator';

@Component({
  selector: 'app-ti',
  templateUrl: './ti.component.html',
  styleUrls: ['./ti.component.css']
})
export class TiComponent implements OnInit {
  durationInSeconds = 5;
  isLinear: boolean = true;
  referenceID: FormGroup;
  firstDose: FormGroup;
  firstVSS: any;
  secondDose: FormGroup;
  secondVSS: any;

  currentDose = "1st";
  currentID = 0;
  vssTable = { "site_address": "", "date": "", "time": "" }
  userTable = { "first_name": "_____", "middle_name": "_", "last_name": "_____", "birthdate": "____-__-__", "sex": "_", "occupation": "_____", "email": "_____", "municipality": "______", "barangay": "_____", "mobile_number": "______" };
  esTable = { "priority": "__", "status": "_____", reason: "..." };
  // esTable = { "priority": "1", "status": "Pending", reason: "Assigned medical personnel has yet to review your application" };
  instructions = "";
  labels = this._api.labels;
  questions = this._api.questions;

  respsTable: MatTableDataSource<any>;
  respsLength: number;
  respsColumns: string[] = this._api.formKeys[3];
  @ViewChild('RespsTable') rtSort: MatSort;
  @ViewChild('RespsPaginator', { static: true }) rtPage: MatPaginator;

  @ViewChild('tabGroup') tabGroup: any;


  /**Grid Tiles**/
  cardLayout = this.BreakpointObserver.observe(Breakpoints.Handset).pipe(
    map(({ matches }) => {
      if (matches) {
        return {
          columns: 2,
          patient_info_card: { cols: 2, rows: 12 },
          vaccination_info_card: { cols: 2, rows: 5 },
          vaccination_sched_card: { cols: 2, rows: 4 },
          instruction_card: { cols: 2, rows: 4 },

        };
      }

      return {
        columns: 14,
        patient_info_card: { cols: 6, rows: 12 },
        vaccination_info_card: { cols: 8, rows: 5 },
        vaccination_sched_card: { cols: 8, rows: 3 },
        instruction_card: { cols: 8, rows: 4 },
      };
    })
  );

  constructor(private _formBuilder: FormBuilder, private _api: ApiService, private BreakpointObserver: BreakpointObserver) { }
  isHandset: Observable<BreakpointState> = this.BreakpointObserver.observe(Breakpoints.Handset)

  ngOnInit(): void {
    this.referenceID = this._formBuilder.group({
      rID: ['', Validators.required]
    });
    this.firstDose = this._formBuilder.group({
      user: [this.currentID, Validators.required],
      dose: ['1st', Validators.required],
      status: ['C', Validators.required],
      session: ['0', Validators.required],
      time: ['None', Validators.required],
      site: ['0', Validators.required],
      serial: ['None', Validators.required],
      batch_number: ['0', Validators.required],
      manufacturer: ['None', Validators.required],
      license_number: [this._api.id, Validators.required],
    });
    this.secondDose = this._formBuilder.group({
      user: [this.currentID, Validators.required],
      dose: ['2nd', Validators.required],
      status: ['C', Validators.required],
      session: ['0', Validators.required],
      time: ['None', Validators.required],
      site: ['0', Validators.required],
      serial: ['None', Validators.required],
      batch_number: ['0', Validators.required],
      manufacturer: ['None', Validators.required],
      license_number: [this._api.id, Validators.required],
    });
  }

  tabChanged() {
    if (this.tabGroup.selectedIndex == 0) {
      this.vssTable = this.firstVSS;
    }
    if (this.tabGroup.selectedIndex == 1) {
      this.vssTable = this.secondVSS;
    }
  }

  search() {
    console.log(this.tabGroup.selectedIndex);
    let id = this.referenceID.controls["rID"].value;
    this.currentID = id;
    this.firstDose.patchValue({ "user": this.currentID });
    this.secondDose.patchValue({ "user": this.currentID });
    this._api.getTracking(id).then((value: any) => {
      let data = this._api.handle(value, 5);
      this._api.getSession(data[0].session).then((value: any) => {
        this.firstVSS = value["query_result"][0];
        this.vssTable = this.firstVSS;
        this._api.getSites(this.firstVSS["session"]).then((value: any) => {
          let address: string = `${value["query_result"][0]["site_address"]}, ${value["query_result"][0]["barangay"]}`;
          this.firstVSS["site_address"] = address;
        });
      });
      this._api.getSession(data[1].session).then((value: any) => {
        this.secondVSS = value;
        this._api.getSites(this.secondVSS["session"]).then((value: any) => {
          let address: string = `${value["query_result"][0]["site_address"]}, ${value["query_result"][0]["barangay"]}`;
          this.secondVSS["site_address"] = address;
        });
      });
      this.firstDose.setValue(data[0]);
      this.secondDose.setValue(data[1]);
    });
    this._api.getProfile(id, true).then((value: any) => {
      this.userTable = value["query_result"][0];
    });
    this._api.getResponse(id).then((value: any) => {
      this.respsTable = new MatTableDataSource(this._api.handle(value, 3)[0]);
      this.respsLength = value["Response"].length;
      this.respsTable.sort = this.rtSort;
      this.respsTable.paginator = this.rtPage;
    });
    this._api.getApplications(id).then((value: any) => {
      this.esTable = value["query_result"][0];
      this.esTable.status = this._api.labels[`${this.esTable.status}`];
    });
  }

  update(dose: string) {
    if (dose === "1st") {
      this._api.putRequest(this.firstDose, 5, this.currentID, dose).then(() => {
        this.firstDose.reset();
        this.secondDose.reset();
        this.userTable = { "first_name": "_____", "middle_name": "_", "last_name": "_____", "birthdate": "____-__-__", "sex": "_", "occupation": "_____", "email": "_____", "municipality": "______", "barangay": "_____", "mobile_number": "______" };
        this.esTable = { "priority": "__", "status": "_____", reason: "..." };
        this.currentID = 0;
        alert("Successfully updated patient's tracking information");
      });
    } else {
      this._api.putRequest(this.secondDose, 5, this.currentID, dose).then(() => {
        this.firstDose.reset();
        this.secondDose.reset();
        this.userTable = { "first_name": "_____", "middle_name": "_", "last_name": "_____", "birthdate": "____-__-__", "sex": "_", "occupation": "_____", "email": "_____", "municipality": "______", "barangay": "_____", "mobile_number": "______" };
        this.esTable = { "priority": "__", "status": "_____", reason: "..." };
        this.currentID = 0;
        alert("Successfully updated patient's tracking information");
      });
    }

  }

  color() {
    let c: string = this.esTable.status.toUpperCase();
    if (c == "PENDING") {
      return "#EC9007";
    }
    if (c == "GRANTED") {
      return "#0BB608";
    }
    if (c == "GRANTED@RISK") {
      return "#0BB608";
    }
    if (c == "DENIED") {
      return "#E23333";
    }
  }
}
