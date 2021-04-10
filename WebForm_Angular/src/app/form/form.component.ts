import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { ApiService } from './../api.service';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-form',
  templateUrl: './form.component.html',
  styleUrls: ['./form.component.scss']
})

export class FormComponent implements OnInit {
  isLinear = true;
  isVerified = false;
  isVerifying = true;
  firstFormGroup: FormGroup;
  secondFormGroup: FormGroup

  private httpOptions = {
    method: 'POST',
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
    }),
  };

  constructor(private _formBuilder: FormBuilder, private _api: ApiService, private _router: Router) { }

  ngOnInit() {

    this.firstFormGroup = this._formBuilder.group({
      first_name: ['Arlan Vincent John', Validators.required],
      middle_name: ['Villaroya', Validators.required],
      last_name: ['German', Validators.required],
      birthdate: ['2001-02-19', Validators.required],
      sex: ['M', Validators.required],
      occupation: ['Student', Validators.required],
      email: ['arlan.german.ag@gmail.com', [Validators.required, Validators.pattern("^.+\@.+$")]],
      mobile_number: ['639995529611', [Validators.required, Validators.pattern("^((\\+63-?)|0)?[0-9]{12}$")]],
      region: ['7', Validators.required],
      province: ['Cebu', Validators.required],
      municipality: ['Lapu-Lapu', Validators.required],
      barangay: ['Agus', Validators.required],
      home_address: ['Blk 16, Lot 5, Bali Subdvision', Validators.required],
    });
    this.secondFormGroup = this._formBuilder.group({
      1: ['N', Validators.required],
      2: ['N', Validators.required],
      3: ['N', Validators.required],
      4: ['N', Validators.required],
      5: ['N', Validators.required],
      6: ['N', Validators.required],
      7: ['N', Validators.required],
      8: ['N', Validators.required],
      9: ['N', Validators.required],
      10: ['N', Validators.required],
      11: ['N', Validators.required],
      12: ['N', Validators.required],
      13: ['N', Validators.required],
      14: ['N', Validators.required],
      15: ['N', Validators.required],
      16: ['N', Validators.required],
      17: ['N', Validators.required],
      18: ['N', Validators.required],
      19: ['N', Validators.required],
      20: ['N', Validators.required],
      21: ['N', Validators.required],
      22: ['N', Validators.required],
      23: ['N', Validators.required],
      24: ['N', Validators.required],
      25: ['N', Validators.required],
      26: ['N', Validators.required],
      27: ['N', Validators.required],
      28: ['N', Validators.required],
      29: ['N', Validators.required],
      30: ['N', Validators.required],
      31: ['N', Validators.required],
      32: ['N', Validators.required],
    });
  }

  async verifyTab() {
    this.isVerifying = true;
    await this._api.verifyRequest(this.firstFormGroup.controls["mobile_number"].value).then(async (value: any) => {
      this.isVerified = value["valid"];
      if (!value["valid"]) {
        window.open("http://developer.globelabs.com.ph/dialog/oauth/dq6eHEReEgCMLTKkEqieqkCGeqojHMAz", 'MS', 'toolbar=no,scrollbars=no,resizable=no,top=100,left=500,width=800,height=1000');
        await this._api.verifyRequest(this.firstFormGroup.controls["mobile_number"].value).then((value: any) => {
          this.isVerified = value["valid"];
        }).catch(() => {
          alert("[TODO] Better Error Display: " + "Mobile number is not subscribed");
        });;
      }
    }).catch(() => {
      alert("[TODO] Better Error Display: " + "Mobile number is not subscribed");
    });
  }

  toggle() {

  }

  get f() {
    return this.firstFormGroup.controls;
  }

  submit() {
    this._api.postRequest({ "personal_information": this.firstFormGroup.value, "response": this.secondFormGroup.value }).then(() => {
      alert("[TODO] Better Success Display: Application successfully sent");
      setTimeout(() => {
        this._router.navigate(["/home"]);
      }, 3000);
    }).catch(() => {
      alert("[TODO] Better Error Display: Server encountered error. Application discarded");
      setTimeout(() => {
        this._router.navigate(["/home"]);
      }, 3000);
    });
  }
}
