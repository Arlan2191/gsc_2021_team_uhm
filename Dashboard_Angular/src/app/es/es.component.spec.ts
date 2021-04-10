import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { EsComponent } from './es.component';

describe('EsComponent', () => {
  let component: EsComponent;
  let fixture: ComponentFixture<EsComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ EsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
