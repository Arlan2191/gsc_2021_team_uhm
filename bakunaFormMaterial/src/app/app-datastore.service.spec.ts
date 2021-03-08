import { TestBed } from '@angular/core/testing';

import { AppDatastoreService } from './app-datastore.service';

describe('AppDatastoreService', () => {
  let service: AppDatastoreService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AppDatastoreService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
