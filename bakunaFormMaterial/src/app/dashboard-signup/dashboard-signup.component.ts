import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, FormControl, Validators, Form} from '@angular/forms';

interface Sex {
  title: string
}

@Component({
  selector: 'app-dashboard-signup',
  templateUrl: './dashboard-signup.component.html',
  styleUrls: ['./dashboard-signup.component.css']
})

export class DashboardSignupComponent implements OnInit {

  labels: Sex[] = [
    {title: 'Female'},
    {title: 'Male'}
  ];

  isLinear = false;
  firstFormGroup: FormGroup;
  secondFormGroup: FormGroup;
  thirdFormGroup: FormGroup;
  fourthFormGroup: FormGroup;
  fifthFormGroup: FormGroup;

  constructor(private _formBuilder: FormBuilder) { }

  ngOnInit(): void {
    this.firstFormGroup = this._formBuilder.group({
        /** PERSONNEL PERSONAL INFO INPUT */
      first_name: ['', Validators.required],
      middle_name: ['', Validators.required],
      last_name: ['', Validators.required],
      birthdate: ['', Validators.required],
      sex: ['', Validators.required],
      occupation: ['', Validators.required],
      
      /** PERSONNEL CONTACT INFO INPUT */
      mobile_number: ['',[Validators.required, Validators.pattern("^((\\+63-?)|0)?[0-9]{11}$")]],
      email: ['', [Validators.required, Validators.email]],
      home_address: ['', Validators.required],
      city: ['', Validators.required],
      barangay: ['', Validators.required],

      /** PERSONNEL ORGANIZATION INFO INPUT */
      prc_license: ['', Validators.required],
      organization: ['', Validators.required],
      organization_telecom: ['', [Validators.required, Validators.pattern('[- +()0-9]{6,}')]],
      organization_email: ['', [Validators.required, Validators.email]],
      organization_address: ['', Validators.required],
      
    });

    this.secondFormGroup = this._formBuilder.group({
      qOne: ['', Validators.required],
      qTwo: ['', Validators.required],
      qThree: ['', Validators.required],
      qFour: ['', Validators.required],
      qFive: ['', Validators.required],
      qSix: ['', Validators.required],
      qSeven: ['', Validators.required],
      qEight: ['', Validators.required],
      qNine: ['', Validators.required],
      qTen: ['', Validators.required],
      qEleven: ['', Validators.required],
      qTwelve: ['', Validators.required],
    });

    this.thirdFormGroup = this._formBuilder.group({
      qThirteen: ['', Validators.required],
      qFourteen: ['', Validators.required],
      qFifteen: ['', Validators.required],
      qSixteen: ['', Validators.required],
      qSeventeen: ['', Validators.required],
      qEighteen: ['', Validators.required],
    });

    this.fourthFormGroup = this._formBuilder.group({
      qNineteen: ['', Validators.required],
      qTwenty: ['', Validators.required],
      qTwentyOne: ['', Validators.required],
      qTwentyTwo: ['', Validators.required],
      qTwentyThree: ['', Validators.required],
      qTwentyFour: ['', Validators.required],
      qTwentyFive: ['', Validators.required],
      qTwentySix: ['', Validators.required],
      qTwentySeven: ['', Validators.required],
      qTwentyEight: ['', Validators.required],
      qTwentyNine: ['', Validators.required],
    });

    this.fifthFormGroup = this._formBuilder.group({
      qThirty: ['', Validators.required],
      qThirtyOne: ['', Validators.required],
      qThirtyTwo: ['', Validators.required],
    });

    
  }

submit(){
  console.log(this.firstFormGroup.value);
  console.log(this.secondFormGroup.value);
}


}
