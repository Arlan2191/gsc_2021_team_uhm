import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  registerFormGroup: FormGroup;
  hide = true;

  constructor(private _formBuilder: FormBuilder, private _http: HttpClient) { }

  ngOnInit(): void {
    this.registerFormGroup = this._formBuilder.group({
      license_number: ['00000000', Validators.required],
      first_name: ['Arlan Vincent John', Validators.required],
      middle_name: ['Villaroya', Validators.required],
      last_name: ['German', Validators.required],
      birthdate: ['2001-02-19', Validators.required],
      sex: ['M', Validators.required],
      occupation: ['Student', Validators.required],
      email: ['arlan.german.ag@gmail.com', [Validators.required, Validators.pattern("^.+\@.+$")]],
      mobile_number: ['639995529611', [Validators.required, Validators.pattern("^((\\+63-?)|0)?[0-9]{12}$")]],
      home_address: ['Blk 16, Lot 5, Bali Subdvision', Validators.required],
      city: ['Lapu-Lapu', Validators.required],
      barangay: ['Agus', Validators.required],
      org: ['Org', Validators.required],
      org_email: ['org@org.com', Validators.required],
      org_telecom: ['+00000000000', Validators.required],
      org_address: ['Org Bldg, Org City, Org', Validators.required]
    });
  }

  submit() {

  }

}
