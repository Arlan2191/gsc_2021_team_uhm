import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DashboardESComponent } from './dashboard-es.component';

describe('DashboardESComponent', () => {
  let component: DashboardESComponent;
  let fixture: ComponentFixture<DashboardESComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DashboardESComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DashboardESComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
