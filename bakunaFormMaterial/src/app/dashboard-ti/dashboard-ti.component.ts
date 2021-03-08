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


@Component({
  selector: 'app-dashboard-ti',
  templateUrl: './dashboard-ti.component.html',
  styleUrls: ['./dashboard-ti.component.css']
})
export class DashboardTIComponent implements OnInit {


  /** LABEL FORM INPUT */
  labelControl = new FormControl('', Validators.required);
  selectFormControl = new FormControl('', Validators.required);
  labels: Label[] = [
    {title: 'complete'},
    {title: 'ineligible'},
    {title: 'waiting'},
    {title: 'pending'},
    {title: 'missed'},
  ];

   /** Based on the screen size, switch from standard to one column per row */
  cardLayout = this.BreakpointObserver.observe(Breakpoints.Handset).pipe(
    map(({ matches }) => {
      if (matches) {
        return {
          columns: 2,
          patient_info_card: { cols: 2, rows: 4 },
          vaccination_info_card: { cols: 2, rows: 5 },
          instruction_card: { cols: 2, rows: 5 },
        };
      }
 
     return {
        columns: 4,
        patient_info_card: { cols: 2, rows: 4 },
        vaccination_info_card: { cols: 2, rows: 4 },
        instruction_card: { cols: 4, rows: 3 },
      };
    })
  );

  isHandset: Observable<BreakpointState> = this.BreakpointObserver.observe(Breakpoints.Handset)
  constructor(private BreakpointObserver: BreakpointObserver) { }

  ngOnInit(): void {
  }

}
