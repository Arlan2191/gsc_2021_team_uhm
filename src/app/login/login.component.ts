import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginFormGroup: FormGroup;
  hide = true;

  constructor(private _formBuilder: FormBuilder, private _http: HttpClient) { }

  ngOnInit(): void {
    this.loginFormGroup = this._formBuilder.group({
      license_number: ['', Validators.required],
      PIN: ['', Validators.required],
    });
  }

}
