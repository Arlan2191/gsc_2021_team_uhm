import { LandingComponent } from './landing/landing.component';
import { AuthGuard } from './auth/auth.guard';
import { TiComponent } from './ti/ti.component';
import { EsComponent } from './es/es.component';
import { RegisterComponent } from './register/register.component';
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { VsComponent } from './vs/vs.component';
import { RegisterlguComponent } from './registerlgu/registerlgu.component';
import { RegisterNavigationComponent } from './register-navigation/register-navigation.component';


const routes: Routes = [
  // { path: '**',
  //   redirectTo: '/home'
  // },
  {
    path: '',
    component: LandingComponent
  },
  {
    path: 'landing',
    component: LandingComponent
  },
  {
    path: 'home',
    component: HomeComponent,
    // canActivate: [AuthGuard]
  },
  {
    path: 'login',
    component: LoginComponent
  },
  {
    path: 'register',
    component: RegisterNavigationComponent
  },
  {
    path: 'register-personnel',
    component: RegisterComponent
  },
  {
    path: 'register-lgu',
    component: RegisterlguComponent
  },
  {
    path: 'review',
    component: EsComponent,
    // canActivate: [AuthGuard]
  },
  {
    path: 'track',
    component: TiComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'session',
    component: VsComponent,
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { relativeLinkResolution: 'legacy' })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
