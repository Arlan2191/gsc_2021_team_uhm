import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { DashboardLoginComponent } from './dashboard-login/dashboard-login.component';
import { DashboardESComponent } from './dashboard-es/dashboard-es.component';
import { FormComponent } from "./form/form.component";
import { HomeComponent } from './home/home.component';
import { DashboardTIComponent } from './dashboard-ti/dashboard-ti.component';
import { DashboardSignupComponent } from './dashboard-signup/dashboard-signup.component';
import { LandingPageFormComponent } from './landing-page-form/landing-page-form.component';


const routes: Routes = [
  {
    path: '',
    component: HomeComponent,
    data: {animation: 'Home'}
  },
  {
    path: 'landing-page-form',
    component: LandingPageFormComponent,
  },
  {
    path: 'form',
    component: FormComponent,
    data: {animation: 'form'}
  },
  {
    path: 'dashboard-login',
    component: DashboardLoginComponent,
  },
  {
    path: 'dashboard-signup',
    component: DashboardSignupComponent,
  },
  {
    path: 'dashboard-es',
    component: DashboardESComponent,
  },
  {
    path: 'dashboard-ti',
    component: DashboardTIComponent,
  },
  {
    path: 'home',
    component: HomeComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
export const routingComponents = [HomeComponent, FormComponent]
