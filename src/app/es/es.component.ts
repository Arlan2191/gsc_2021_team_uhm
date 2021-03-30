import { ApiService } from './../api.service';
import { FormService } from './../form.service';
import { Component, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { SelectionModel } from '@angular/cdk/collections';
import { BreakpointObserver, Breakpoints, BreakpointState } from '@angular/cdk/layout';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators'; 

@Component({
  selector: 'app-es',
  templateUrl: './es.component.html',
  styleUrls: ['./es.component.css']
})
export class EsComponent implements OnInit {
  currentID: number;
  reviewFormGroup: FormGroup;
  siteFormGroup: FormGroup;
  siteEditFormGroup: FormGroup;
  showResponse: boolean = false;
  allowEdit: boolean = false;
  selection: any = new SelectionModel<any>(true, []);

  appsTable: MatTableDataSource<any>;
  appsColumns: string[] = this._api.formKeys[0];
  @ViewChild('AppsTable') atSort: MatSort;

  respsTable: MatTableDataSource<any>;
  respsColumns: string[] = this._api.formKeys[3];
  @ViewChild('RespsTable') rtSort: MatSort;

  sitesTable: MatTableDataSource<any>;
  sitesColumns: string[] = this._api.formKeys[1];
  @ViewChild('SitesTable') stSort: MatSort;

  userTable: MatTableDataSource<any>;
  userColumns: string[] = this._api.formKeys[2];


  /*Grid Tiles*/
  /** Based on the screen size, switch from standard to one column per row */
  cardLayout = this.BreakpointObserver.observe(Breakpoints.Handset).pipe(
    map(({ matches }) => {
      if (matches) {
        return {
          columns: 3,
          pending_application__card: { cols: 3, rows: 4 },
          user_information_card: { cols: 3, rows: 4 },
          review_card: { cols: 3, rows: 4 },
          questionnaire_response_card: { cols: 3, rows: 8},
        };
      }
 
     return {
        columns: 12,
        pending_application__card: { cols: 3, rows: 4 },
        user_information_card: { cols: 9, rows: 8 },
        review_card: { cols: 3, rows: 4 },
        questionnaire_response_card: { cols: 12, rows: 3},
      };
    })
  );


  constructor(private _formBuilder: FormBuilder, private _api: ApiService, private BreakpointObserver: BreakpointObserver) { }
  isHandset: Observable<BreakpointState> = this.BreakpointObserver.observe(Breakpoints.Handset)

  ngOnInit() {
    this._api.getApplications().then((data) => {
      this.appsTable = new MatTableDataSource(this._api.handle(data, 0)[0]);
      this.appsTable.sort = this.atSort;
    });
    this._api.getSites().then((data) => {
      this.sitesTable = new MatTableDataSource(this._api.handle(data, 1)[0]);
      this.sitesTable.sort = this.stSort;
    });
    this.reviewFormGroup = this._formBuilder.group({
      status: ['G', Validators.required],
      reason: ['Some Reason', Validators.required]
    });
    this.siteFormGroup = this._formBuilder.group({
      site_address: ['Some Address', Validators.required],
      date: ['2021-03-14', Validators.required],
      time: ['15:24:16', Validators.required],
      city: ['Lapu-Lapu', Validators.required],
      barangay: ['Agus', Validators.required]
    });
    this.siteEditFormGroup = this._formBuilder.group({
      site_address: ['', Validators.required],
      date: ['', Validators.required],
      time: ['', Validators.required],
      city: ['', Validators.required],
      barangay: ['', Validators.required]
    });
  }

  async getPI(id: number) {
    this.currentID = id;
    this.showResponse = true;
    await this._api.getProfile(id).then((data) => {
      this.userTable = new MatTableDataSource(this._api.handle(data, 2)[0]);
    });
    await this._api.getResponse(id).then((data) => {
      this.respsTable = new MatTableDataSource(this._api.handle(data, 3)[0]);
      this.respsTable.sort = this.rtSort;
    });
  }

  submit() {
    this._api.putRequest(this.reviewFormGroup, 0, this.currentID.toString()).then(() => {
      console.log("Success");
    });
    if (this.reviewFormGroup.controls["status"].value == "G" || this.reviewFormGroup.controls["status"].value == "G@R") {
      this._api.postRequest(4, this._formBuilder.group({ user: this.currentID.toString(), dose: '1st' })).then(() => {
        console.log("Success");
      });
      this._api.postRequest(4, this._formBuilder.group({ user: this.currentID.toString(), dose: '2nd' })).then(() => {
        console.log("Success");
      });
    }
  }

  add() {
    this._api.postRequest(1, this.siteFormGroup).then(() => {
      console.log("Success");
    })
  }

  match(id: number) {
    if (this.selection.selected.length == 1 && this.allowEdit) {
      return id == this.selection.selected[0]['id'];
    }
    return false;
  }

  edit() {
    if (this.selection.selected.length == 1) {
      this.allowEdit = true;
      let selected = this.selection.selected[0];
      this.siteEditFormGroup = this._formBuilder.group({
        site_address: [selected["site_address"], Validators.required],
        date: [selected["date"], Validators.required],
        time: [selected["time"], Validators.required],
        city: [selected["city"], Validators.required],
        barangay: [selected["barangay"], Validators.required]
      });
    }
  }

  cancel() {
    this.allowEdit = false;
  }

  save() {
    let selected = this.selection.selected[0];
    this._api.putRequest(this.siteEditFormGroup, 1, selected["id"]).then(() => {
      console.log("Success");
    });
    this.allowEdit = false;
  }

  isAllSelected() {
    const numSelected = this.selection.selected.length;
    const numRows = this.sitesTable.data.length;
    return numSelected === numRows;
  }

  masterToggle() {
    this.isAllSelected() ?
      this.selection.clear() :
      this.sitesTable.data.forEach(row => this.selection.select(row));
  }

  delete() {
    this._api.deleteSite(this.selection.selected).then(() => {
      console.log("Success");
    });
  }

}
