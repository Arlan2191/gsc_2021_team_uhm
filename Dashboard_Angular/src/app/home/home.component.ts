import { Component, OnInit } from '@angular/core';
import { BreakpointObserver, Breakpoints, BreakpointState } from '@angular/cdk/layout';
import { Observable } from 'rxjs';
import { LoaderService } from 'src/app/loader/loader.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  constructor(private breakpointObserver: BreakpointObserver,
    public loaderService: LoaderService) { }
  isHandset: Observable<BreakpointState> = this.breakpointObserver.observe(Breakpoints.Handset)
  ngOnInit(): void {
  }

}
