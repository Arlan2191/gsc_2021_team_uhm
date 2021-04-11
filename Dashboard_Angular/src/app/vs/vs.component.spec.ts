import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VsComponent } from './vs.component';

describe('VsComponent', () => {
  let component: VsComponent;
  let fixture: ComponentFixture<VsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ VsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(VsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
