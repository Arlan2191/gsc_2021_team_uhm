import { ApiService } from '../api/api.service';
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
import { MatPaginator } from '@angular/material/paginator';

export interface Label {
  value: string;
  title: string;
}

@Component({
  selector: 'app-es',
  templateUrl: './es.component.html',
  styleUrls: ['./es.component.scss']
})
export class EsComponent implements OnInit {
  durationInSeconds = 5;
  currentID: number;
  reviewFormGroup: FormGroup;
  siteFormGroup: FormGroup;
  siteEditFormGroup: FormGroup;
  showResponse: boolean = false;
  allowEdit: boolean = false;
  selection: any = new SelectionModel<any>(true, []);

  appsTable: MatTableDataSource<any>;
  appsColumns: string[] = this._api.formKeys[0];
  appsLength: number;
  @ViewChild('AppsPaginator', { static: true }) atPage: MatPaginator;
  @ViewChild('AppsTable') atSort: MatSort;

  respsTable: MatTableDataSource<any>;
  respsColumns: string[] = this._api.formKeys[3];
  respsLength: number;
  @ViewChild('RespsPaginator', { static: true }) rtPage: MatPaginator;
  @ViewChild('RespsTable') rtSort: MatSort;

  sitesTable: MatTableDataSource<any>;
  sitesColumns: string[] = this._api.formKeys[1];
  sitesLength: number;
  @ViewChild('SitesPaginator', { static: true }) stPage: MatPaginator;
  @ViewChild('SitesTable') stSort: MatSort;

  userTable = this._api.nullValues[2];
  questions = this._api.questions;
  labels = [{ label: "G", value: "GRANTED" }, { label: "G@R", value: "GRANTED@RISK" }, { label: "W", value: "WAITLISTED" }, { label: "P", value: "PENDING" }, { label: "D", value: "DENIED" }];

  /*Grid Tiles*/
  /** Based on the screen size, switch from standard to one column per row */
  cardLayout = this.BreakpointObserver.observe(Breakpoints.Handset).pipe(
    map(({ matches }) => {
      if (matches) {
        return {
          columns: 3,
          pending_application__card: { cols: 3, rows: 6 },
          user_information_card: { cols: 3, rows: 4 },
          review_card: { cols: 3, rows: 4 },
          questionnaire_response_card: { cols: 3, rows: 8 },
        };
      }

      return {
        columns: 12,
        pending_application__card: { cols: 3, rows: 6 },
        user_information_card: { cols: 9, rows: 10 },
        review_card: { cols: 3, rows: 4 },
        questionnaire_response_card: { cols: 12, rows: 6 },
      };
    })
  );


  constructor(private _formBuilder: FormBuilder, private _api: ApiService, private BreakpointObserver: BreakpointObserver) { }
  isHandset: Observable<BreakpointState> = this.BreakpointObserver.observe(Breakpoints.Handset)

  ngOnInit() {
    this._api.getApplications().then((data) => {
      this.appsLength = data["query_result"].length;
      this.appsTable = new MatTableDataSource(this._api.handle(data, 0)[0]);
      this.appsTable.sort = this.atSort;
      this.appsTable.paginator = this.atPage;
    });
    this._api.getSites().then((data) => {
      this.sitesLength = data["query_result"].length;
      this.sitesTable = new MatTableDataSource(this._api.handle(data, 1)[0]);
      this.sitesTable.sort = this.stSort;
      this.sitesTable.paginator = this.stPage;
    });
    this.reviewFormGroup = this._formBuilder.group({
      status: ['G', Validators.required],
      reason: ['Some Reason', Validators.required]
    });
    this.siteFormGroup = this._formBuilder.group({
      site_address: ['Some Address', Validators.required],
      barangay: ['Agus', Validators.required]
    });
    this.siteEditFormGroup = this._formBuilder.group({
      site_address: ['', Validators.required],
      barangay: ['', Validators.required]
    });
  }

  async getPI(id: number) {
    this.currentID = id;
    this.showResponse = true;
    await this._api.getProfile(id).then((data) => {
      this.userTable = this._api.handle(data, 2);
    });
    await this._api.getResponse(id).then((data) => {
      this.respsLength = data["Response"].length;
      this.respsTable = new MatTableDataSource(this._api.handle(data, 3)[0]);
      this.respsTable.sort = this.rtSort;
      this.respsTable.paginator = this.rtPage;
    });
  }

  submit() {
    this._api.putRequest(this.reviewFormGroup, 0, this.currentID).then(() => {
      alert("Successfully updated patient's eligibility profile onto database");
    });
    if (this.reviewFormGroup.controls["status"].value == "G" || this.reviewFormGroup.controls["status"].value == "G@R") {
      this._api.postRequest(4, this._formBuilder.group({ user: this.currentID.toString(), dose: '1st' })).then(() => {
        alert("Successfully updated patient's 1st tracking profile onto database");
      });
      this._api.postRequest(4, this._formBuilder.group({ user: this.currentID.toString(), dose: '2nd' })).then(() => {
        alert("Successfully updated patient's 2nd tracking profile onto database");
      });
    }
  }

  add() {
    this._api.postRequest(1, this.siteFormGroup).then(() => {
      alert("Successfully added onto database");
    })
  }

  match(id: number) {
    if (this.selection.selected.length == 1 && this.allowEdit) {
      return id == this.selection.selected[0]['site_id'];
    }
    return false;
  }

  edit() {
    if (this.selection.selected.length == 1) {
      this.allowEdit = true;
      let selected = this.selection.selected[0];
      this.siteEditFormGroup = this._formBuilder.group({
        site_address: [selected.site_address, Validators.required],
        barangay: [selected.barangay, Validators.required]
      });
    }
  }

  cancel() {
    this.allowEdit = false;
  }

  save() {
    let selected = this.selection.selected[0];
    console.log(this.siteEditFormGroup);
    this._api.putRequest(this.siteEditFormGroup, 1, selected.site_id).then(() => {
      alert("Successfully updated vaccination site");
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
      alert("Successfully removed from database");
    });
  }

}


