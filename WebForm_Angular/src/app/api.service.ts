import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private BASEURL = "http://localhost:8000";

  private httpOptions = {
    method: 'POST',
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
    }),
  };
  constructor(private _http: HttpClient) { }

  async verifyRequest(mobile_number: string) {
    return await this._http.post(`${this.BASEURL}/site/otp`, JSON.stringify({ "mobile_number": mobile_number }), this.httpOptions).toPromise();
  }

  async postRequest(data: any) {
    return await this._http.post(`${this.BASEURL}/forms/submit`, JSON.stringify(data), this.httpOptions).toPromise();
  }
}
