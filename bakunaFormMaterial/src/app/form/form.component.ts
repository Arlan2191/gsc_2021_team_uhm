import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './form.component.html',
  styleUrls: ['./form.component.scss']
})

export class FormComponent implements OnInit {
  title = 'bakunaFormMaterial';

  isLinear = true;
  firstFormGroup: FormGroup;
  secondFormGroup: FormGroup
  thirdFormGroup: FormGroup;
  
  constructor(private _formBuilder: FormBuilder) {}
  
  ngOnInit() {

    this.firstFormGroup = this._formBuilder.group({
      firstName: ['', Validators.required],
      middleName: ['', Validators.required],
      lastName: ['', Validators.required],
      birthdate: ['', Validators.required],
      sex: ['', Validators.required],
      mobileNumber: ['', [Validators.required, Validators.pattern("^((\\+63-?)|0)?[0-9]{11}$")]],
      homeAddress: ['', Validators.required],
      city: ['', Validators.required],
      barangay: ['', Validators.required]
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
      qThirteen: ['', Validators.required],
      qFourteen: ['', Validators.required],
      qFifteen: ['', Validators.required],
      qSixteen: ['', Validators.required],
      qSeventeen: ['', Validators.required],
      qEighteen: ['', Validators.required],
      
    });
    this.thirdFormGroup = this._formBuilder.group({
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
      qThirty: ['', Validators.required],
      qThirtyOne: ['', Validators.required],
      qThirtyTwo: ['', Validators.required],
      
    });

  }
  
  get f(){
    return this.firstFormGroup.controls;
  }

  submit(){
      console.log(this.firstFormGroup.value);
      console.log(this.secondFormGroup.value);
  }




}