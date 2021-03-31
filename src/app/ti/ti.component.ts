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
  secondDose: FormGroup;

  userTable: MatTableDataSource<any>;
  userColumns: string[] = this._api.formKeys[6];

  esTable: MatTableDataSource<any>;
  esColumns: string[] = this._api.formKeys[0];

  respsTable: MatTableDataSource<any>;
  respsColumns: string[] = this._api.formKeys[3];
  @ViewChild('RespsTable') rtSort: MatSort;


  /**Grid Tiles**/
   cardLayout = this.BreakpointObserver.observe(Breakpoints.Handset).pipe(
    map(({ matches }) => {
      if (matches) {
        return {
          columns: 2,
          patient_info_card: { cols: 2, rows: 12 },
          vaccination_info_card: { cols: 2, rows: 5 },
          vaccination_sched_card: { cols: 2, rows: 4},
          instruction_card: { cols: 2, rows: 4 },

        };
      }
 
     return {
        columns: 14,
        patient_info_card: { cols: 6, rows: 12 },
        vaccination_info_card: { cols: 8, rows: 5 },
        vaccination_sched_card: { cols: 8, rows: 3},
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
      user: ['', Validators.required],
      dose: ['', Validators.required],
      status: ['', Validators.required],
      date: ['', Validators.required],
      time: ['', Validators.required],
      site: ['', Validators.required],
      serial: ['', Validators.required],
      batch_number: ['', Validators.required],
      manufacturer: ['', Validators.required],
      license_number: ['', Validators.required],
    });
    this.secondDose = this._formBuilder.group({
      user: ['', Validators.required],
      dose: ['', Validators.required],
      status: ['', Validators.required],
      date: ['', Validators.required],
      time: ['', Validators.required],
      site: ['', Validators.required],
      serial: ['', Validators.required],
      batch_number: ['', Validators.required],
      manufacturer: ['', Validators.required],
      license_number: ['', Validators.required],
    });
  }

  search() {
    let id = this.referenceID.controls["rID"].value;
    this._api.getTracking(id).then((value: any) => {
      let data = this._api.handle(value, 5);
      this.firstDose.setValue(data[0]);
      this.secondDose.setValue(data[1]);
    });
    this._api.getUserProfile(id).then((value: any) => {
      let data = this._api.handle(value, 6);
      this.userTable = new MatTableDataSource([data[0]["personal_information"]]);
      this.respsTable = new MatTableDataSource(data[1]["response"]["Response"]);
      this.respsTable.sort = this.rtSort;
      this.esTable = new MatTableDataSource([data[2]["eligibility_status"]]);
      console.log(data);
    });
  }

  update() {

  }


}
