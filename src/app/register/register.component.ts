import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';

export interface Label {
  value: string;
  title: string;
}

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  registerFormGroup: FormGroup;
  hide = true;

  regions: Label[] = [
    {value: 'NCR', title: 'NCR'},
    {value: 'CAR', title: 'CAR'},
    {value: 'I', title: 'I - Ilocos Region'},
    {value: 'II', title: 'II - Cagayan Valley'},
    {value: 'III', title: 'III - Central Luzon '},
    {value: 'IVA', title: 'IVA - CALABARZON'},
    {value: 'IVB', title: 'IVB - MIMAROPA / Southwestern Tagalog'},
    {value: 'V', title: 'V - Bicol Region'},
    {value: 'VI', title: 'VI - Western Visayas'},
    {value: 'VII', title: 'VII - Central Visayas'},
    {value: 'VIII', title: 'VIII - Eastern Visayas'},
    {value: 'IX', title: 'IX - Zamboanga Peninsula'},
    {value: 'X', title: 'X - Northern Mindanao'},
    {value: 'XI', title: 'XI - Davao Region'},
    {value: 'XII', title: 'XII - SOCCSKARGEN'},
    {value: 'XIII', title: 'XIII - Caraga Region'},
    {value: 'BARMM', title: 'BARMM'},
  ];

  provinces: Label[] = [
    {value: 'Cebu', title:'Cebu'}
  ];

  sex: Label[] = [
    {value: 'M', title:'Male'},
    {value: 'F', title:'Female'}
  ]

  


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
      region: ['VII', Validators.required],
      province: ['Cebu', Validators.required],
      municipality: ['Lapu-Lapu', Validators.required],
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
