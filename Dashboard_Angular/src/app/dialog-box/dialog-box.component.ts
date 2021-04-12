import { Component, OnInit,  Inject, Optional } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';

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
  vs_id: number;
  site_id: number;
}

@Component({
  selector: 'app-dialog-box',
  templateUrl: './dialog-box.component.html',
  styleUrls: ['./dialog-box.component.css']
})
export class DialogBoxComponent {

  AddSessionFormGroup: FormGroup;
  action:string;
  local_data:any;

  constructor(
    public dialogRef: MatDialogRef<DialogBoxComponent>,
    //Prevent error if no data is passed
    @Optional() @Inject(MAT_DIALOG_DATA) public data: UsersData,
    private _formBuilder: FormBuilder, private _http: HttpClient) {
    console.log(data);
    this.local_data = {...data};
    this.action = this.local_data.action;
  }

  ngOnInit() {
    this.AddSessionFormGroup = this._formBuilder.group({
      time: ['', Validators.required],
      max_cap: ['', Validators.required],
      target_barangay: ['', Validators.required],
      birth_range1: ['', Validators.required],
      birth_range2: ['', Validators.required],
      priority: ['', Validators.required],
      date: ['', Validators.required],
      vs_id: ['', Validators.required],
      site_id: ['', Validators.required]
    });
  }

  doAction(){
    this.dialogRef.close({event:this.action,data:this.local_data});
  }

  closeDialog(){
    this.dialogRef.close({event:'Cancel'});
  }

}