import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { MatDialogModule } from '@angular/material/dialog';
import {MatCardModule} from '@angular/material/card';
import { AppRoutingModule, routingComponents } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatStepperModule } from '@angular/material/stepper';
import {MatInputModule} from '@angular/material/input';
import { FlexLayoutModule } from '@angular/flex-layout';
import { MatButtonModule } from '@angular/material/button';
import { MatListModule } from '@angular/material/list';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatRadioModule } from '@angular/material/radio';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon';
import { HomeComponent } from './home/home.component';
import { MatSidenavModule } from '@angular/material/sidenav';
import { LoginDialogComponent } from './login-dialog/login-dialog.component';
import { DashboardESComponent } from './dashboard-es/dashboard-es.component';
import {MatDividerModule} from '@angular/material/divider';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatSortModule } from '@angular/material/sort';
import { DashboardLoginComponent } from './dashboard-login/dashboard-login.component';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatMenuModule } from '@angular/material/menu';
import { LayoutModule } from '@angular/cdk/layout';
import { DashboardTIComponent } from './dashboard-ti/dashboard-ti.component';
import { CardComponent } from './card/card.component';
import { MatSelectModule } from '@angular/material/select';
import {NgxMaterialTimepickerModule} from 'ngx-material-timepicker';
import { DashboardSignupComponent } from './dashboard-signup/dashboard-signup.component';
import { LandingPageFormComponent } from './landing-page-form/landing-page-form.component';
import { MatTabsModule } from '@angular/material/tabs';

@NgModule({
  declarations: [
    AppComponent,
    routingComponents,
    HomeComponent,
    LoginDialogComponent,
    DashboardESComponent,
    DashboardLoginComponent,
    DashboardTIComponent,
    CardComponent,
    DashboardSignupComponent,
    LandingPageFormComponent,
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatStepperModule,
    FormsModule,
    MatGridListModule,
    ReactiveFormsModule,
    MatInputModule,
    MatButtonModule,
    MatPaginatorModule,
    MatSortModule,
    MatListModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatButtonToggleModule,
    MatCheckboxModule,
    MatFormFieldModule,
    MatRadioModule,
    MatCardModule,
    MatToolbarModule,
    MatIconModule,
    MatSidenavModule,
    FlexLayoutModule,
    MatDialogModule,
    MatDividerModule,
    MatTableModule,
    MatMenuModule,
    LayoutModule,
    MatSelectModule,
    NgxMaterialTimepickerModule,
    MatTabsModule

  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
