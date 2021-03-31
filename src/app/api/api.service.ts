import { Form, FormGroup } from '@angular/forms';
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private BASEURL = "";
  private urlKey = ["ES", "VS"];
  private nullValues = [
    { "id": 0, "status": 0, "reason": "N/A" },
    { "id": 0, "site_address": "N/A", "barangay": "N/A", "city": "N/A" },
    { 'id': 0, 'birthdate': '0000-00-00', 'sex': 'N/A', 'occupation': 'N/A', 'city': 'N/A', 'barangay': 'N/A' },
    { 'num': 0, 'question': 'N/A', 'answer': 'N/A' },
    { 'dose': 0, 'user': 0, 'status': 'N/A', 'batch_number': 'N/A', 'date': 'N/A', 'time': 'N/A', 'site': 'N/A', 'manufacturer': 'N/A', 'license_number': 'N/A', 'serial': 'N/A' },
    { 'first_name': 'N/A', 'middle_name': 'N/A', 'last_name': 'N/A', 'birthdate': 'N/A', 'sex': 'N/A', 'occupation': 'N/A', 'email': 'N/A', 'mobile_number': 'N/A', 'city': 'N/A', 'barangay': 'N/A' }
  ];
  formKeys = [
    ["id", "status", "reason"],
    ['select', 'id', 'site_address', 'date', 'time', 'barangay', 'city'],
    ['id', 'birthdate', 'sex', 'occupation', 'city', 'barangay'],
    ['num', 'question', 'answer'],
    ['user', 'dose'],
    ['dose', 'user', 'status', 'batch_number', 'date', 'time', 'site', 'manufacturer', 'license_number', 'serial'],
    ['first_name', 'middle_name', 'last_name', 'birthdate', 'sex', 'occupation', 'email', 'mobile_number', 'city', 'barangay']
  ];

  private httpOptions = {
    method: 'POST',
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
    }),
  };

  constructor(private _http: HttpClient) { }

  async getApplications() {
    return await this._http.get<Array<any>>(`${this.BASEURL}/site/table?name=ES`).toPromise();
  }

  async getSites() {
    return await this._http.get<Array<any>>(`${this.BASEURL}/site/table?name=VS`).toPromise();
  }

  async getProfile(id: number) {
    return await this._http.get<Array<any>>(`${this.BASEURL}/site/table?name=PI&id=${id}`).toPromise();
  }

  async getUserProfile(id: number) {
    return await this._http.get<JSON>(`${this.BASEURL}/site/GET/Profile/${id}`).toPromise();
  }

  async getResponse(id: number) {
    return await this._http.get<Array<any>>(`${this.BASEURL}/site/datastore?id=${id}`).toPromise();
  }

  async getTracking(id: number) {
    return await this._http.get<Array<any>>(`${this.BASEURL}/site/table?name=TI&id=${id}`).toPromise();
  }

  handle(data: any, table_code: number) {
    if (table_code == 3) {
      if (data["query_result"]["Response"].length) {
        return [data["query_result"]["Response"]];
      } else {
        return [[this.nullValues[3]]];
      }
    } else if (table_code == 5) {
      if (data["query_result"].length == 2) {
        return [data["query_result"][0], data["query_result"][1]]
      } else {
        return [[this.nullValues[4]]];
      }
    } else if (table_code == 6) {
      if (data["query_result"].length == 3) {
        return [data["query_result"][0], data["query_result"][1], data["query_result"][2]]
      } else {
        return [[this.nullValues[5]], this.nullValues[3], this.nullValues[0]];
      }
    } else {
      if (data["query_result"].length) {
        return [data["query_result"]];
      } else {
        return [[this.nullValues[table_code]]];
      }
    }
  }

  async postRequest(table_code: number, formGroup: FormGroup) {
    let formData = new FormData();
    this.formKeys[table_code].forEach((value: string) => {
      if (value != "id" && value != "num" && value != "select") {
        formData.append(value, formGroup.controls[value].value);
      }
    });
    if (table_code == 1) {
      return await this._http.post(`${this.BASEURL}/site-api/POST/VS`, formData).toPromise();
    } else if (table_code == 4) {
      return await this._http.post(`${this.BASEURL}/site-api/POST/TI`, formData).toPromise()
    }
  }

  async putRequest(formGroup: FormGroup, table_code: number, id?: string, dose?: string) {
    let formData = new FormData();
    this.formKeys[table_code].forEach((value: string) => {
      if (value != "id" && value != "num" && value != "select") {
        formData.append(value, formGroup.controls[value].value)
      }
    });
    if (id) {
      return await this._http.post(`${this.BASEURL}/site-api/PUT/${this.urlKey[table_code]}/${id}`, formData).toPromise();
    }
  }

  async deleteSite(sites: Array<any>) {
    let siteIDs: Array<any>;
    sites.forEach((value) => {
      siteIDs.push(value["id"]);
    });
    return await this._http.post(`${this.BASEURL}/site-api/DELETE`, JSON.stringify({ "delete_query": siteIDs }), this.httpOptions).toPromise();
  }
}
