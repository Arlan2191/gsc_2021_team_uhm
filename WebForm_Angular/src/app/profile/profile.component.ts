import { Component } from '@angular/core';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent {
  x: Window;

  constructor() { }

  ngOnInit() {

  }

  verifyTab() {
    this.x = window.open("http://developer.globelabs.com.ph/dialog/oauth/dq6eHEReEgCMLTKkEqieqkCGeqojHMAz", 'MSISDN Verification', 'toolbar=no,scrollbars=no,resizable=no,top=100,left=500,width=800,height=1000');
    // console.log(x.document.baseURI);
  }

  viewNumber() {
    console.log(this.x.location.href)
  }
}
