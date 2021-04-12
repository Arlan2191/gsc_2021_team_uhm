import { MatStepper } from '@angular/material/stepper';
import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api/api.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';

export interface Label {
  value: string;
  title: string;
}

@Component({
  selector: 'app-registerlgu',
  templateUrl: './registerlgu.component.html',
  styleUrls: ['./registerlgu.component.css']
})
export class RegisterlguComponent implements OnInit {

  registerFormGroup: FormGroup;
  formError: string;

  regions: Label[] = [
    { value: 'NCR', title: 'NCR' },
    { value: 'CAR', title: 'CAR' },
    { value: 'I', title: 'I - Ilocos Region' },
    { value: 'II', title: 'II - Cagayan Valley' },
    { value: 'III', title: 'III - Central Luzon ' },
    { value: 'IVA', title: 'IVA - CALABARZON' },
    { value: 'IVB', title: 'IVB - MIMAROPA / Southwestern Tagalog' },
    { value: 'V', title: 'V - Bicol Region' },
    { value: 'VI', title: 'VI - Western Visayas' },
    { value: 'VII', title: 'VII - Central Visayas' },
    { value: 'VIII', title: 'VIII - Eastern Visayas' },
    { value: 'IX', title: 'IX - Zamboanga Peninsula' },
    { value: 'X', title: 'X - Northern Mindanao' },
    { value: 'XI', title: 'XI - Davao Region' },
    { value: 'XII', title: 'XII - SOCCSKARGEN' },
    { value: 'XIII', title: 'XIII - Caraga Region' },
    { value: 'BARMM', title: 'BARMM' },
  ];

  provinces: Label[] = [
    { value: 'Cebu', title: 'Cebu' }
  ];

  username: string;
  password: string;

  constructor(private _formBuilder: FormBuilder, private _api: ApiService, private _router: Router) { }

  ngOnInit(): void {
    this.registerFormGroup = this._formBuilder.group({
      organization: ['Org', Validators.required],
      organization_email: ['org@org.com', Validators.required],
      organization_telecom: ['+00000000000', Validators.required],
      organization_region: ['VII', Validators.required],
      organization_province: ['Cebu', Validators.required],
      organization_municipality: ['Lapu-Lapu', Validators.required],
      organization_barangay: ['Agus', Validators.required],
      organization_address: ['Org Bldg, Org City, Org', Validators.required]
    });
  }

  submit(stepper: MatStepper) {
    this._api.postRequest(7, this.registerFormGroup).then((token: any) => {
      if (Object.keys(token).includes("user")) {
        this.username = token["user"]["username"];
        this.password = token["user"]["PIN"];
        stepper.next();
      } else {
        alert("[TODO] Specific Error Handling: " + token["errors"]["error"]);
        this.registerFormGroup.reset();
      }
    }).catch(() => {
      this.formError = "Server encountered an error, please try again later.";
    });
  }

  proceed() {
    this._router.navigate(["/login"]);
  }

}
