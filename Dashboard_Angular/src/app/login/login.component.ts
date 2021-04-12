import { ApiService } from './../api/api.service';
import { Router } from '@angular/router';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';

type IFocus = 'none' | 'left' | 'right' | 'bumpLeft' | 'bumpRight';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent implements OnInit {
  loginFormGroup: FormGroup;
  hide = true;

  constructor(private _formBuilder: FormBuilder, private _api: ApiService, private _router: Router) { }

  ngOnInit(): void {
    this.loginFormGroup = this._formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required],
    });
  }

  login() {
    this._api.loginRequest(this.loginFormGroup.getRawValue()).then((v: any) => {
      if (v != undefined) {
        this._api.token = "Token " + v.user.token;
        this._api.id = v.user.id;
        this._router.navigate(["/home"]);
      }
    }).catch(() => {
      alert("[TODO] Better Error Display: " + "Invalid Username and Password");
    });
  }

}
