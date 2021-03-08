import { Component, OnInit } from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import { LoginDialogComponent } from 'src/app/login-dialog/login-dialog.component';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {

  constructor(public dialog: MatDialog) { }

openDialog(): void {
  const dialogRef = this.dialog.open(LoginDialogComponent, {
  });

  dialogRef.afterClosed().subscribe(result => {
    console.log('The dialog was closed');
  });
}

  ngOnInit(): void {
  }

}
