import { ApiService } from './api.service';
import { Injectable } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Injectable({
  providedIn: 'root'
})
export class FormService {

  constructor(private _formBuilder: FormBuilder, private _api: ApiService) { }

  async initApplications() {
    let apps;
    await this._api.getApplications().then((data: any) => {
      apps = data;
    });
    return apps;
  }

  initSites() {

  }

  initProfile() {

  }

  initResponse() {

  }
}
