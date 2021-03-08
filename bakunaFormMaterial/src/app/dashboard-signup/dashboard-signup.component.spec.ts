import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DashboardSignupComponent } from './dashboard-signup.component';

describe('DashboardSignupComponent', () => {
  let component: DashboardSignupComponent;
  let fixture: ComponentFixture<DashboardSignupComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DashboardSignupComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DashboardSignupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
