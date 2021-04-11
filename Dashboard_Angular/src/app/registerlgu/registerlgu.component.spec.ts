import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RegisterlguComponent } from './registerlgu.component';

describe('RegisterlguComponent', () => {
  let component: RegisterlguComponent;
  let fixture: ComponentFixture<RegisterlguComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RegisterlguComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RegisterlguComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
