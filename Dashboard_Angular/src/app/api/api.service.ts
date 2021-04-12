import { Form, FormGroup } from '@angular/forms';
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private BASEURL = "http://localhost:8000";
  private urlKey = ["ES", "VS", "TI", "VSS"];
  nullValues = [
    { "id": 0, "status": 0 },
    { "site_id": 0, "site_address": "N/A", "barangay": "N/A" },
    { 'id': 0, 'birthdate': '0000-00-00', 'sex': 'N/A', 'occupation': 'N/A', 'barangay': 'N/A', "municipality": "N/A" },
    { 'num': 0, 'question': 'N/A', 'answer': 'N/A' },
    { 'dose': 0, 'user': 0, 'status': 'N/A', 'batch_number': 'N/A', 'session': 'N/A', 'time': 'N/A', 'site': 'N/A', 'manufacturer': 'N/A', 'license_number': 'N/A', 'serial': 'N/A' },
    { 'first_name': 'N/A', 'middle_name': 'N/A', 'last_name': 'N/A', 'birthdate': 'N/A', 'sex': 'N/A', 'occupation': 'N/A', 'email': 'N/A', 'mobile_number': 'N/A', 'municipality': 'N/A', 'barangay': 'N/A' },
    { 'date': 'N/A', 'time': 'N/A' },
  ];
  formKeys = [
    ["id", "status"],
    ['select', 'site_id', 'site_address', 'barangay'],
    ['id', 'birthdate', 'sex', 'occupation', 'barangay', "municipality"],
    ['num', 'question', 'answer'],
    ['user', 'dose'],
    ['dose', 'user', 'status', 'batch_number', 'session', 'time', 'site', 'manufacturer', 'license_number', 'serial'],
    ['first_name', 'middle_name', 'last_name', 'birthdate', 'sex', 'occupation', 'email', 'mobile_number', 'municipality', 'barangay'],
    ["license_number", "first_name", "middle_name", "last_name", "birthdate", "sex", "occupation", "email", "mobile_number", "organization", "organization_email", "organization_telecom", "organization_region", "organization_province", "organization_municipality", "organization_barangay", "organization_address"],
    ['date', 'time']
  ];
  questions = {
    "1": "Nagpositibo ka na ba sa COVID-19?",
    "2": "Sa nakaraang 14 na araw, may nakasama ka na ba na positibo sa COVID-19?",
    "3": "Sa nakaraang 14 na araw, nanggaling ka ba sa ibang bansa?",
    "4": "Nakisalamuha ka ba sa maraming tao sa pagtitipon sa nakaraang 2 linggo?",
    "5": "May Lagnat ng isa o mahigit pang araw sa nakaraang 2 linggo",
    "6": "May Ubo ng isa o mahigit pang araw sa nakaraang 2 linggo",
    "7": "May Sipon ng isa o mahigit pang araw sa nakaraang 2 linggo",
    "8": "May Sorethroat ng isa o mahigit pang araw sa nakaraang 2 linggo",
    "9": "May Pananakit ng Katawan ng isa o mahigit pang araw sa nakaraang 2 linggo",
    "10": "May Kawalan ng pang amoy at panlasa ng isa o mahigit pang araw sa nakaraang 2 linggo",
    "11": "May Hingal/hirap sa paghinga ng isa o mahigit pang araw sa nakaraang 2 linggo",
    "12": "May Pagtatae ng isa o mahigit pang araw sa nakaraang 2 linggo",
    "13": "Nakagat ka ba ng aso sa nakaraang 4 na linggo at nabakunahan?",
    "14": "Nabakunahan ka ba ng Covid-19 Vaccine sa nakaraang 4 na linggo?",
    "15": "Sinasalinan ka ba ng dugo?",
    "16": "Umiinom ka ba ng Prednisone / Steroids o antiviral drugs?",
    "17": "May allergy sa latex, pagkain, gamot o sa bakuna?",
    "18": "Nagkaroon ng malalang reaksyon pagkatapos mabakunahan?",
    "19": "Mayroon / nagkaroon nang Sakit sa baga",
    "20": "Mayroon / nagkaroon nang Sakit sa puso",
    "21": "Mayroon / nagkaroon nang Hika",
    "22": "Mayroon / nagkaroon nang Sakit sa Bato",
    "23": "Mayroon / nagkaroon nang Diabetes",
    "24": "Mayroon / nagkaroon nang Altapresyon",
    "25": "Mayroon / nagkaroon nang Sakit sa Dugo",
    "26": "Mayroon / nagkaroon nang Cancer",
    "27": "Mayroon / nagkaroon nang Leukemia",
    "28": "Mayroon / nagkaroon nang Organ Transplant",
    "29": "Mayroon / nagkaroon nang Sakit sa pagiisip / Seizure disorder",
    "30": "Buntis o may planong magbuntis sa darating na buwan?",
    "31": "Nagpapasuso ka ba?",
    "32": "Kasama ka ba sa COVID-19 Clinical Study?",
  };
  labels = { "G": "GRANTED", "G@R": "GRANTED@RISK", "D": "DENIED", "W": "WAITLISTED", "P": "PENDING" }
  token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjUiLCJleHAiOjE2MTgyMTIxNTJ9.j7NNjefl12923Smw_EP4zbsdA16aCVYbJgkjsZpzirs";
  id = "";
  constructor(private _http: HttpClient) { }

  async getApplications(id?: number) {
    if (id == undefined) {
      return await this._http.get<Array<any>>(`${this.BASEURL}/site/table?name=ES`, {
        headers: new HttpHeaders({
          "Authorization": this.token,
        })
      }).toPromise();
    }
    return await this._http.get<Array<any>>(`${this.BASEURL}/site/table?name=ES&id=${id}`, {
      headers: new HttpHeaders({
        "Authorization": this.token,
      })
    }).toPromise();
  }

  async getSites(id?: number) {
    if (id) {
      return await this._http.get<Array<any>>(`${this.BASEURL}/site/table?name=VS&id=${id}`, {
        headers: new HttpHeaders({
          "Authorization": this.token,
        })
      }).toPromise();
    }
    return await this._http.get<Array<any>>(`${this.BASEURL}/site/table?name=VS`, {
      headers: new HttpHeaders({
        "Authorization": this.token,
      })
    }).toPromise();
  }

  async getSession(id: number) {
    return await this._http.get<Array<any>>(`${this.BASEURL}/site/table?name=VSS&id=${id}`, {
      headers: new HttpHeaders({
        "Authorization": this.token,
      })
    }).toPromise();
  }

  async getProfile(id: number, isProfile?: boolean) {
    if (isProfile === true) {
      return await this._http.get<Array<any>>(`${this.BASEURL}/site/table?name=PI&id=${id}&isProfile=${isProfile}`, {
        headers: new HttpHeaders({
          "Authorization": this.token,
        })
      }).toPromise();
    } else {
      return await this._http.get<Array<any>>(`${this.BASEURL}/site/table?name=PI&id=${id}`, {
        headers: new HttpHeaders({
          "Authorization": this.token,
        })
      }).toPromise();
    }
  }

  async getResponse(id: number) {
    return await this._http.get<Array<any>>(`${this.BASEURL}/site/datastore?name=MHR&id=${id}`, {
      headers: new HttpHeaders({
        "Authorization": this.token,
      })
    }).toPromise();
  }

  async getTracking(id: number) {
    return await this._http.get<Array<any>>(`${this.BASEURL}/site/table?name=TI&id=${id}`, {
      headers: new HttpHeaders({
        "Authorization": this.token,
      })
    }).toPromise();
  }

  handle(data: any, table_code: number) {
    if (table_code == 3) {
      if (data["Response"].length) {
        let temp = [];
        data["Response"].forEach((e) => {
          temp.push({ "num": e.num, "question": this.questions[`${e.num}`], "answer": e.answer });
        });
        return [temp];
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
    } else if (table_code == 2) {
      if (data["query_result"].length == 1) {
        return data["query_result"][0];
      } else {
        return this.nullValues[2];
      }
    } else if (table_code == 1) {
      if (data["query_result"].length) {
        let temp = [];
        data["query_result"].forEach(e => {
          temp.push({ site_id: e.site_id, barangay: e.barangay, site_address: e.site_address })
        });
        return [temp];
      } else {
        return this.nullValues[1];
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
    this.formKeys[table_code].forEach((v: string) => {
      if (v != "id" && v != "num" && v != "select") {
        formData.append(v, formGroup.controls[v].value);
        console.log(v, formGroup.controls[v].value);
      }
    });
    if (table_code == 1) {
      return await this._http.post(`${this.BASEURL}/site/table?name=VS`, formData, {
        headers: new HttpHeaders({
          "Authorization": this.token,
        })
      }).toPromise();
    } else if (table_code == 4) {
      return await this._http.post(`${this.BASEURL}/site/table?name=TI`, formData, {
        headers: new HttpHeaders({
          "Authorization": this.token,
        })
      }).toPromise();
    } else if (table_code == 7) {
      return await this._http.post(`${this.BASEURL}/site/staff`, formData, {
        headers: new HttpHeaders({
          "Authorization": this.token,
        })
      }).toPromise();
    }
  }

  async putRequest(formGroup: FormGroup, table_code: number, id: number, dose?: string) {
    let formData = new FormData();
    this.formKeys[table_code].forEach((v: string) => {
      if (v != "id" && v != "num" && v != "select") {
        formData.append(v, formGroup.controls[v].value);
      }
    });
    if (id && dose == undefined) {
      if (table_code == 0) {
        formData.append("reason", formGroup.controls["reason"].value);
      }
      return await this._http.put(`${this.BASEURL}/site/table?name=${this.urlKey[table_code]}&id=${id}`, formData, {
        headers: new HttpHeaders({
          "Authorization": this.token,
        })
      }).toPromise();
    } else if (id && dose != undefined) {
      return await this._http.put(`${this.BASEURL}/site/table?name=TI&id=${id}&dose=${dose}`, formData, {
        headers: new HttpHeaders({
          "Authorization": this.token,
        })
      }).toPromise();
    }
  }

  async deleteSite(sites: Array<any>) {
    let siteIDs: Array<any>;
    sites.forEach((value) => {
      siteIDs.push(value["site_id"]);
    });
    return await this._http.post(`${this.BASEURL}/site-api/DELETE`, JSON.stringify({ "delete_query": siteIDs }), {
      headers: new HttpHeaders({
        "Content-Type": "application/json",
        "Authorization": this.token,
      })
    }).toPromise();
  }

  async loginRequest(data: any) {
    return await this._http.post(`${this.BASEURL}/auth/users/login`, JSON.stringify({ "user": data }), {
      headers: new HttpHeaders({
        "Content-Type": "application/json",
        "Authorization": this.token,
      })
    }).toPromise();
  }
}
