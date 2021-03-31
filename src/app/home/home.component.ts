import { Component, OnInit } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Observable } from 'rxjs';
import { LoaderService } from 'src/app/loader/loader.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  constructor(private breakpointObserver: BreakpointObserver, 
    public loaderService:  LoaderService) { }

  ngOnInit(): void {
  }

}
