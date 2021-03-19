import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TiComponent } from './ti.component';

describe('TiComponent', () => {
  let component: TiComponent;
  let fixture: ComponentFixture<TiComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TiComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TiComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
