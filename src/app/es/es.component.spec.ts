import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EsComponent } from './es.component';

describe('EsComponent', () => {
  let component: EsComponent;
  let fixture: ComponentFixture<EsComponent>;

  beforeEach(async(() => {
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
