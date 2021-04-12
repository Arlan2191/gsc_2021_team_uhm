import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RegisterNavigationComponent } from './register-navigation.component';

describe('RegisterNavigationComponent', () => {
  let component: RegisterNavigationComponent;
  let fixture: ComponentFixture<RegisterNavigationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RegisterNavigationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RegisterNavigationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
