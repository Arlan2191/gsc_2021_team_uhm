import { Component, OnInit, Inject, Optional } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

export interface UsersData {
  barangay: string,
  site_address: string
}

@Component({
  selector: 'app-dialog-site',
  templateUrl: './dialog-site.component.html',
  styleUrls: ['./dialog-site.component.css']
})
export class DialogSiteComponent implements OnInit {

  AddSessionFormGroup: FormGroup;
  action: string;
  local_data: any;

  constructor(
    public dialogRef: MatDialogRef<DialogSiteComponent>,
    //Prevent error if no data is passed
    @Optional() @Inject(MAT_DIALOG_DATA) public data: UsersData,
    private _formBuilder: FormBuilder) {
    this.local_data = { ...data };
    this.action = this.local_data.action;
  }

  ngOnInit() {
    this.AddSessionFormGroup = this._formBuilder.group({
      barangay: ['', Validators.required],
      site_address: ['', Validators.required],
    });
  }

  doAction() {
    this.dialogRef.close({ event: this.action, data: this.local_data });
  }

  closeDialog() {
    this.dialogRef.close({ event: 'Cancel' });
  }

}
