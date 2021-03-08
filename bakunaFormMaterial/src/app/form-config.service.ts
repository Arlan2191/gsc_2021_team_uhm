import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class FormConfigService {

  private formConfig: any;
  private http : HttpClient;

  constructor(http: HttpClient) {
        this.http = http;
   }

   
}
