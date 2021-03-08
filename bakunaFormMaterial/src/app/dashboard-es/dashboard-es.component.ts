import { Component, OnInit, ViewChild } from '@angular/core';
import { BreakpointObserver, Breakpoints, BreakpointState } from '@angular/cdk/layout';
import {FormControl, Validators} from '@angular/forms';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';
import { MatPaginator, PageEvent } from '@angular/material/paginator';
import { map } from 'rxjs/operators'; 
import { Observable } from 'rxjs';

export interface Label {
  title: string;
}

export interface Priority {
  title: string;
}

export interface PatientStatus {
  id: number;
  date: string;
  visitTime: string;
  doctor: string;
  conditions: string;
  status: string;
}

export interface PatientPersonalInfo {
  id: number;
  first_name: string;
  last_name: string;
  middle_name: string;
  birthdate: string;
  sex: string; 
  occupation: string; 
  email: string;
  mobile_number: string; 
  home_address: string;
  city: string;
  barangay: string;
}


const PATIENTSTATUS_DATA: PatientStatus[] = [
  {id: 12345,  date: '10/10/2020', visitTime: '09:15-09:45am', doctor:'Dr.Jacob Jimenez', conditions: 'None', status: 'granted'},
  {id: 23456,  date: '10/10/2020', visitTime: '09:15-10:45am', doctor:'Dr.Jacob Jimenez', conditions: 'None', status: 'granted'},
  {id: 34567,  date: '10/10/2020', visitTime: '09:15-10:45am', doctor:'Dr.Jacob Jimenez', conditions: 'None', status: 'granted'},
  {id: 45678,  date: '10/10/2020', visitTime: '09:15-10:45am', doctor:'Dr.Jacob Jimenez', conditions: 'None', status: 'granted'},
  {id: 56789,  date: '10/10/2020', visitTime: '09:15-10:45am', doctor:'Dr.Jacob Jimenez', conditions: 'None', status: 'granted'},
  {id: 67890,  date: '10/10/2020', visitTime: '09:15-10:45am', doctor:'Dr.Jacob Jimenez', conditions: 'None', status: 'granted'},
  {id: 17892,  date: '10/10/2020', visitTime: '09:15-09:45am', doctor:'Dr.Jacob Jimenez', conditions: 'None', status: 'granted'},
  {id: 28934,  date: '10/10/2020', visitTime: '09:15-09:45am', doctor:'Dr.Jacob Jimenez', conditions: 'None', status: 'granted'},
  {id: 34956,  date: '10/10/2020', visitTime: '09:15-09:45am', doctor:'Dr.Jacob Jimenez', conditions: 'None', status: 'granted'},
];

@Component({
  selector: 'app-dashboard-es',
  templateUrl: './dashboard-es.component.html',
  styleUrls: ['./dashboard-es.component.css']
})
export class DashboardESComponent implements OnInit {

    /** LABEL FORM INPUT */
    labelControl = new FormControl('', Validators.required);
    selectFormControl = new FormControl('', Validators.required);
    labels: Label[] = [
      {title: 'granted'},
      {title: 'granted@risk'},
      {title: 'denied'},
      {title: 'waitlistes'},
      {title: 'pending'},
    ];

    /** PRIORITY FORM INPUT w/Scroll */
    priorities: string[] = [ '1st Priority', '2nd Priority', '3rd Priority',
        '4th Priority', '5th Priority', '6th Priority', '7th Priority', '8th Priority',
        '9th Priority', '10th Priority', '11th Priority', '12th Priority']

    /** VACCINATION SCHEDULE INPUT */
    address = new FormControl('', [Validators.required]);
    date = new FormControl('', [Validators.required]);

    getErrorMessage() {
      if (this.address.hasError('required')) {
        return 'You must enter a value';
      }

      if (this.date.hasError('required')) {
        return 'You must pick a date';
      }
    }

    /** Based on the screen size, switch from standard to one column per row */
  cardLayout = this.BreakpointObserver.observe(Breakpoints.Handset).pipe(
    map(({ matches }) => {
      if (matches) {
        return {
          columns: 2,
          patient_info_card: { cols: 2, rows: 2 },
          instruction_card: { cols: 2, rows: 5 },
          med_history_card: { cols: 2, rows: 2},
          table: { cols: 2, rows: 5 },
        };
      }
 
     return {
        columns: 4,
        patient_info_card: { cols: 2, rows: 2 },
        instruction_card: { cols: 2, rows: 4 },
        med_history_card: { cols: 2, rows: 2},
        table: { cols: 4, rows: 4 },
      };
    })
  );

  /** TABLE  */
  dataSource: MatTableDataSource<PatientPersonalInfo>
  @ViewChild(MatPaginator) paginator: MatPaginator;

  isHandset: Observable<BreakpointState> = this.BreakpointObserver.observe(Breakpoints.Handset)
  constructor(private BreakpointObserver: BreakpointObserver) {
      this.patientStatusDataSource = new MatTableDataSource;
   }

  displayedColumnsOne: string[] = ['id','date','visitTime', 'doctor', 'conditions','status'];
  @ViewChild('TableOnePaginator', {static: true}) tableOnePaginator: MatPaginator;
  @ViewChild('TableOneSort', {static: true}) tableOneSort: MatSort;
  patientStatusDataSource: MatTableDataSource<PatientStatus>;

  /*MatPaginator Input*/
  length = 100;
  pageSize = 10;
  pageSizeOptions: number[] = [5, 10, 25, 100];

  /*MatPaginator Output*/
  pageEvent: PageEvent;

  setPageSizeOptions(setPageSizeOptionsInput: string) {
    if(setPageSizeOptionsInput) {
      this.pageSizeOptions = setPageSizeOptionsInput.split(',').map(str => +str);
    }
  }
  
  ngOnInit(): void {
    this.patientStatusDataSource.data = PATIENTSTATUS_DATA;
    this.patientStatusDataSource.paginator = this.tableOnePaginator;
    this.patientStatusDataSource.sort = this.tableOneSort;

  }

  ngAfterViewInit() {
    this.patientStatusDataSource.paginator = this.paginator;
  }

  // applyFilterOne(filterValue: string) {
  //   this.patientStatusDataSource.filter = filterValue.trim().toLowerCase();
  // }

}
