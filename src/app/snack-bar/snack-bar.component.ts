import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-snack-bar',
  templateUrl: './snack-bar.component.html',
  styleUrls: ['./snack-bar.component.css']
})
export class SnackBarComponent implements OnInit {

  constructor(public snackBar: MatSnackBar) { }


  openSnackBar(message: string, action: string, className: string) {

    this.snackBar.open(message, action, {
     duration: 2000,
     verticalPosition: 'top',
     horizontalPosition: 'end',
     panelClass: [className],
   });
  }

  ngOnInit(): void {
  }

}
