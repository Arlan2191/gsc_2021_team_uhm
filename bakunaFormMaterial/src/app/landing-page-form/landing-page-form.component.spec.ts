import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LandingPageFormComponent } from './landing-page-form.component';

describe('LandingPageFormComponent', () => {
  let component: LandingPageFormComponent;
  let fixture: ComponentFixture<LandingPageFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LandingPageFormComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(LandingPageFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
