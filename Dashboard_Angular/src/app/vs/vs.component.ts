import { DialogSiteComponent } from './../dialog-site/dialog-site.component';
import { ApiService } from '../api/api.service';
import { FormService } from './../form.service';
import { Component, OnInit, ViewChild, ChangeDetectorRef } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource, MatTable } from '@angular/material/table';
import { SelectionModel } from '@angular/cdk/collections';
import { BreakpointObserver, Breakpoints, BreakpointState } from '@angular/cdk/layout';
import { MatDialog } from '@angular/material/dialog';
import { DialogBoxComponent } from '../dialog-box/dialog-box.component';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { DateAdapter, MAT_DATE_FORMATS, MAT_DATE_LOCALE } from '@angular/material/core';
import { MomentDateOnlyAdapter } from './moment-utc-adapter';
import { MomentConstructor, Moment } from './moment-date-only';
import { MatPaginator } from '@angular/material/paginator';

export interface Label {
  value: string;
  title: string;
}

export interface UsersData {
  time: string;
  max_cap: number;
  target_barangay: string;
  birth_range1: string;
  birth_range2: string;
  priority: string;
  date: string;
  site_id: number;
}

@Component({
  selector: 'app-vs',
  templateUrl: './vs.component.html',
  styleUrls: ['./vs.component.scss']
})
export class VsComponent implements OnInit {

  durationInSeconds = 5;
  currentID: number;
  siteFormGroup: FormGroup;
  siteEditFormGroup: FormGroup;
  sessionFormGroup: FormGroup;
  showResponse: boolean = false;
  allowEdit: boolean = false;
  selection: any = new SelectionModel<any>(true, []);
  displayedColumns: string[] = ['vs_id', 'date', 'time', 'max_cap', 'target_barangay', 'birth_range', 'priority', 'site_id', 'action'];
  dataSource: any;

  sitesTable: MatTableDataSource<any>;
  sitesColumns: string[] = this._api.formKeys[1];
  sitesLength: number;
  @ViewChild('SitesTable') stSort: MatSort;
  @ViewChild('SitesPaginator', { static: true }) stPage: MatPaginator;

  sessionTable: MatTableDataSource<any>;
  sessionColumns: string[] = this._api.formKeys[9];
  sessionLength: number;
  @ViewChild('SessionsTable') ssSort: MatSort;
  @ViewChild('SessionsPaginator', { static: true }) ssPage: MatPaginator;

  labels: Label[] = [
    { value: 'G', title: 'Granted' },
    { value: 'G@R', title: 'Granted@Risk' },
    { value: 'D', title: 'Denied' },
    { value: 'W', title: 'Waitlisted' },
    { value: 'P', title: 'Pending' },
  ];


  /*Grid Tiles*/
  /** Based on the screen size, switch from standard to one column per row */
  cardLayout = this.BreakpointObserver.observe(Breakpoints.Handset).pipe(
    map(({ matches }) => {
      if (matches) {
        return {
          columns: 4,
          questionnaire_response_card: { cols: 4, rows: 10 },
          vaccination_session_card: { cols: 12, rows: 3 },
        };
      }

      return {
        columns: 12,
        questionnaire_response_card: { cols: 12, rows: 8 },
        vaccination_session_card: { cols: 12, rows: 8 },
      };
    })
  );

  @ViewChild(MatTable, { static: true }) table: MatTable<any>;
  constructor(private _formBuilder: FormBuilder, private _api: ApiService, private BreakpointObserver: BreakpointObserver, public dialog: MatDialog, private changeDetectorRefs: ChangeDetectorRef) { }
  isHandset: Observable<BreakpointState> = this.BreakpointObserver.observe(Breakpoints.Handset)



  ngOnInit() {
    this._api.getSites().then((data) => {
      this.sitesLength = data["query_result"].length;
      this.sitesTable = new MatTableDataSource(this._api.handle(data, 1)[0]);
      this.sitesTable.sort = this.stSort;
      this.sitesTable.paginator = this.stPage;
    });
    this._api.getSessions().then((value: any) => {
      this.sessionLength = value["query_result"].length;
      this.sessionTable = new MatTableDataSource(this._api.handle(value, 9)[0]);
      this.sessionTable.sort = this.ssSort;
      this.sessionTable.paginator = this.ssPage;
    });
    this.siteFormGroup = this._formBuilder.group({
      site_address: ['Some Address', Validators.required],
      barangay: ['Agus', Validators.required]
    });
    this.siteEditFormGroup = this._formBuilder.group({
      site_address: ['', Validators.required],
      barangay: ['', Validators.required]
    });
    this.sessionFormGroup = this._formBuilder.group({
      time: ['', Validators.required],
      max_cap: ['', Validators.required],
      target_barangay: ['', Validators.required],
      birth_range1: ['', Validators.required],
      birth_range2: ['', Validators.required],
      priority: ['', Validators.required],
      date: ['', Validators.required],
      site_id: ['', Validators.required],
    });
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
        site_address: [selected["site_address"], Validators.required],
        barangay: [selected["barangay"], Validators.required]
      });
    }
  }

  cancel() {
    this.allowEdit = false;
  }

  save() {
    let selected = this.selection.selected[0];
    this._api.putRequest(this.siteEditFormGroup, 1, selected["site_id"]).then(() => {
      alert("Successfully saved into database");
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
    this.selection.forEach((e: number) => {
      this._api.deleteSite(e).then(() => {
        alert("Successfully deleted from database");
      });
    });

  }

  openDialog(action, obj) {
    obj.action = action;
    const dialogRef = this.dialog.open(DialogBoxComponent, {
      width: '250px',
      data: obj
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result.event == 'Add') {
        this.addRowData(result.data);
      } else if (result.event == 'Delete') {
        this.deleteRowData(result.data);
      }
    });
  }

  openDialog2(action, obj) {
    obj.action = action;
    const dialogRef = this.dialog.open(DialogSiteComponent, {
      width: '250px',
      data: obj
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result.event == 'Add') {
        this.addRowData2(result.data);
      }
    });
  }

  addRowData(row_obj) {
    this.sessionFormGroup.setValue({
      date: JSON.stringify(row_obj.date).slice(1, 11),
      time: row_obj.time,
      max_cap: row_obj.max_cap,
      target_barangay: row_obj.target_barangay,
      birth_range1: JSON.stringify(row_obj.birth_range1).slice(1, 11),
      birth_range2: JSON.stringify(row_obj.birth_range2).slice(1, 11),
      priority: row_obj.priority,
      site_id: row_obj.site_id,
    });
    this.table.renderRows();
    this._api.postRequest(9, this.sessionFormGroup).then(() => {
      alert("Successfully added into database");
    });
  }

  deleteRowData(row_obj) {
    this.dataSource = this.dataSource.filter((value, key) => {
      return value.vs_id != row_obj.vs_id;
    });
  }

  addRowData2(row_obj) {
    console.log(row_obj);
    this.siteFormGroup.setValue({
      barangay: row_obj.barangay,
      site_address: row_obj.site_address,
    });
    this.table.renderRows();
    this._api.postRequest(1, this.siteFormGroup).then(() => {
      alert("Successfully added into database");
    });
  }
}
