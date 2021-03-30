import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { ScreenMovementAnimation } from './split-screen.animation';

type IFocus = 'none' | 'left' | 'right' | 'bumpLeft' | 'bumpRight';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
  animations: ScreenMovementAnimation
})
export class LoginComponent implements OnInit {
  loginFormGroup: FormGroup;
  hide = true;

  private _focus: IFocus = 'none';

  public set focus (move: IFocus) {
    this._focus = move;
    console.log(move);
  }

  public get focus(): IFocus { return this._focus; }
  constructor(private _formBuilder: FormBuilder, private _http: HttpClient) { }

  ngOnInit(): void {
    this.loginFormGroup = this._formBuilder.group({
      license_number: ['', Validators.required],
      PIN: ['', Validators.required],
    });
  }

  
  shouldBump(callingSide: 'left' | 'right'): boolean {
    return (this.focus === 'right' && callingSide === 'left') ||
           (this.focus === 'left' && callingSide === 'right');
  }

  shouldResetBump(callingSide: 'left' | 'right'): boolean {
    return (this.focus === 'bumpRight' && callingSide === 'left') ||
           (this.focus === 'bumpLeft' && callingSide === 'right');
  }

  handleBump(callingSide: 'left' | 'right') {
    if (this.shouldBump(callingSide) || this.shouldResetBump(callingSide)) {
      switch(this.focus) {
        case 'right':
          this.focus = 'bumpLeft';
          break;
        case 'bumpRight':
          // moving into 'right' => 'bumpRight', then moving into 'left', reset to 'left'
          this.focus = 'left'
          break;
        case 'left':
          this.focus = 'bumpRight';
          break;
        case 'bumpLeft':
          // moving into 'left' => 'bumpLeft', then moving into 'right', reset to 'right'
          this.focus = 'right';
          break;
      }
    }
  }
}
