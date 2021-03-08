import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DashboardTIComponent } from './dashboard-ti.component';

describe('DashboardTIComponent', () => {
  let component: DashboardTIComponent;
  let fixture: ComponentFixture<DashboardTIComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DashboardTIComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DashboardTIComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
