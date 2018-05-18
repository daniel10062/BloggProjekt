console.log('Loading sketch.js');

var score = 0;
var highscoreNewGame;
var ship;
var powerup;
var p;
var p2;
var p3;
var p4;
var playerPart = [];
var invaderPart = [];
var img = [];
var canvas;
var invaders = [];
var invader;
var level = 1;
var startinv = 8;
var maxlength = 10;
var nYval = 100;
var b = 0;
var textfield = false;
var life = 3;
var invaderkills = 0;
var button0;
var button1;
var button2;
var buttonpause;
var buttonUnpause;
var menuimg = document.getElementById('Menuimg');
var gameoverimg = document.getElementById('gameoverimg');
var gameover = document.getElementById('gameover');
var highscoreimg = document.getElementById('highscoreimg');
var highscore = document.getElementById('highscore');
var pausescreenimg = document.getElementById('Pausescreenimg');
var pausescreen = document.getElementById('Pausescreen');
var menuBackground;
var powerups = [];
var switchtogameover = true;
var bosslevels = 4;
var ispaused = false;
var highscoreValue;

const STATE_PREGAME = 1;
const STATE_RUNNING = 2;
const STATE_GAME_OVER = 3;
const STATE_PAUSED = 4;
const STATE_HIGHSCORE = 5;

var gameState = STATE_PREGAME;


//------------------------------------------------------------//
// dö vid en viss närhet av ship
// Bossar vid specifika levelsit re
// Bossens hitbox
// Fixa google chrome api så man kan lagra variable i webläsaren
//------------------------------------------------------------//
window.setInterval(function(){
  /// call your function here
  invadershoot();
}, 1000 - (level * 500));

window.setInterval(function(){
  /// call your function here

  createpower();
}, 8000);

window.setInterval(function(){
  /// call your function here

  allowshoot();
}, 750);

window.setInterval(function(){
  /// call your function here

  setDoubleShoot();
}, 9000);


function createpower() {
  if (!(powerup)) {
    powerup = new PowerUp();
  }
}

function setDoubleShoot() {
  if (ship.doubleshoot === true) {
    ship.doubleshoot = false;
  }
}

function allowshoot() {
  ship.allowshoot = !ship.allowshoot;
}

function randomIntFromInterval(min,max)
{
  return Math.floor(Math.random()*(max-min+1)+min);
}

function invadershoot() {
  if (!ispaused) {
    var a = floor(randomIntFromInterval(0,invaders.length));
    if (invaders[a]) {
      invaderPart.push(new Particle(invaders[a].x, invaders[a].y + 21, 3.5));
    }
  }
}
function highscoretext() {
  if (!textfield) {
    p = createP(highscoreValue);
    p.position(420,-8);
    p.id('ptag');

    p2 = createP(score);
    p2.position(390,135);
    p2.id('ptag2');

    p3 = createP(level);
    p3.position(710,135);
    p3.id('ptag3');

    p4 = createP('Unknown');
    p4.position(8,135);
    p4.id('ptag4');

    textfield = true;
  }
}

function changetoHighscore() {
  //Show score reached, level reached and player name
  if (button2) {
    button2.remove();
    button2 = undefined;
  }

  gameover.style.display = 'none';
  gameoverimg.style.display = 'none';
  highscore.style.display = 'inline';
  highscoreimg.style.display = 'inline';
}

function gameoverscreen() {
  gameover.style.display = 'inline';
  gameoverimg.style.display = 'inline';

  if (!button1) {
    button1 = createButton('new game');
    button1.position(width/4 + 60 ,height/2 + 7.5);
    button1.mousePressed(resetclear);
    button1.id('newgameButton');
  }
  if (!button2) {
    button2 = createButton('highscore');
    button2.position(width/2 + 20,height/2 + 7);
    button2.mousePressed(gamestateChange);
    button2.id('highscoreButton');
  }

function gamestateChange() {
  textfield = false;
  gameState = STATE_HIGHSCORE;
}

}
function resetclear() {
  //button1.parentNode.removeChild(button1);
  //button2.parentNode.removeChild(button2);
  if (p && p2 && p3 && p4) {
    p.remove();
    p2.remove();
    p3.remove();
    p4.remove();
    p = undefined;
    p2 = undefined;
    p3 = undefined;
    p4 = undefined;
}

  button1.remove();
  if (button2) {
    button2.remove();
    button2 = undefined;
  }
  gameover.style.display = 'none';
  gameoverimg.style.display = 'none';
  highscore.style.display = 'none';
  highscoreimg.style.display = 'none';
  resetGame();
  gameState = STATE_RUNNING;
  button1 = undefined;
}

function windowResized() {
  function windowResized() {
    resizeCanvas(windowWidth,windowHeight);
  }
}

function resetGame() {
  //button.style.display = 'none';
  nYval = 150;
  score = 0;
  level = 1;
  b = 0;
  life = 3;
  startinv = 8;

  highscore.style.display = 'none';
  highscoreimg.style.display = 'none';
  gameover.style.display = 'none';
  gameoverimg.style.display = 'none';

  if (invaders) {
    invaders = new Array();
  }

  if (invaderPart) {
    invaderPart = [];
  }

  ship = new Ship();
  createinvaders();
}

function changebackground() {
    menuBackground.style.display = 'none';
    button0.remove();
    resetGame();
    gameState = STATE_RUNNING;
}

function scorecontroller() {
  textSize(16);
  text('Points' + ' ' + score ,width - 120, 20);
  fill(0, 105, 255);
}
function lifecontroller() {
  textSize(16);
  text('Lifes' + ' ' + life ,25, 20);
  fill(255);
}
function changetopause() {
  if (gameState === STATE_PAUSED) {
    buttonUnpause.remove();
    buttonpause = undefined;
    ispaused = false;
    pausescreen.style.display = 'none';
    pausescreenimg.style.display = 'none';
    gameState = STATE_RUNNING;
  } else {
    buttonpause.remove();
    buttonUnpause = undefined;
    gameState = STATE_PAUSED;
  }
}

function preload() {
  img[0] = loadImage('../static/Pictures/bakgrund.jpg');
  img[1] = loadImage('../static/Pictures/Skott_bla.png');
  img[2] = loadImage('../static/Pictures/Skott.png');
  img[3] = loadImage('../static/Pictures/Fiende.png');
  img[4] = loadImage('../static/Pictures/powerup.png');
  img[5] = loadImage('../static/Pictures/ship.png');
  img[6] = loadImage('../static/Pictures/Boss.png');
  menuBackground = document.getElementById('backgroundimage');

  if (localStorage.getItem('highscoreValue') === undefined || isNaN(localStorage.getItem('highscoreValue'))) {
    localStorage.setItem('highscoreValue', 0);
  }
}
function setup() {
  // put setup code here
  canvas = createCanvas(800,500);
  canvas.position(0,0);
  canvas.style('z-index', '-2');
  //resetGame();
}


function draw() {
  // put drawing code here
  if (gameState === STATE_PREGAME) {
    if (!button0) {
      button0 = createButton('Start');
      button0.position(width/10 - 30,height/6);
      button0.mousePressed(changebackground);
      button0.id('startButton');
    }
  }
  else if (gameState === STATE_RUNNING) {
    if (!buttonpause) {
      buttonpause = createButton('Pause');
      buttonpause.id('buttonPause');
      buttonpause.position(width - 125,25);
      buttonpause.mousePressed(changetopause);
    }

    background(51);
    image(img[0], 0,0, width, height);
    ship.show();
    scorecontroller();
    lifecontroller();
    //drawing the PowerUp
    if (powerup) {
      if (powerup.okey === false) {
        window.setInterval(function(){
          powerup.powerupChange();
        }, 7500);
      }
      if (powerup.okey === true) {
        powerup.show();
        powerup.move();
        powerup.check();
        if (powerup.edgeR || powerup.edgeL) {
          powerup.shift();
        }
      }
    }

    // check if player hits the powerup and if so give buff
    if (playerPart && powerup) {
      for (var i = 0; i < playerPart.length; i++) {
        if ((playerPart[i].hit(powerup.x, powerup.y + playerPart[i].r)) || (playerPart[i].hit(powerup.x + playerPart[i].r, powerup.y))) {
          ship.doubleshoot = true;
          powerup.okey = false;
        }
      }
    }

    if (invaders.length < 1) {
      level += 1;
      nYval = 150;
      b = 0;
      startinv = startinv + (level + 2);
      createinvaders();
    }

    for (var i = 0; i < invaders.length; i++) {
      if (invaders[i].y >= height - 60 || life === 0) {
        gameState = STATE_GAME_OVER;
      }
      if (invaders[i].lifes < 1) {
        if (bosslevels == level) {
          bosslevels *= 2;
        } else {
          invaders.splice(i,1);
        }
      } else {
        invaders[i].show();
        invaders[i].move();
        invaders[i].swapcheck();

        if (invaders[i].edgeR || invaders[i].edgeL) {
          invaders[i].shift();
        }
      }
    }

    for (var p = 0; p < invaderPart.length; p++) {
      if (invaderPart[p].hit(ship.x - 7, height - 50)) {
        life = life - 1;
        invaderPart[p].deleteparticle = true;
      } else if (invaderPart[p].y > height) {
        invaderPart[p].deleteparticle = true;
      }
    }

    if (playerPart.length > 0) {
      for (var i = 0; i < playerPart.length; i++) {
        for (var j = 0; j < invaders.length; j++) {
          if ((playerPart[i].hit(invaders[j].x - 7.5, invaders[j].y))) {
            score = score + 100;
            playerPart[i].deleteparticle = true;
            invaders[j].lifes = invaders[j].lifes - 1;
            invaderkills += 1;
            //invaders.splice(j, 1);
          } else if (playerPart[i].y < 0) {
            playerPart[i].deleteparticle = true;
          }
        }
      }
    }


    for (var i = 0; i < playerPart.length; i++) {
      playerPart[i].playerPartShow();
      playerPart[i].move();
    }
    for (var c = 0; c < invaderPart.length; c++) {
      invaderPart[c].invaderPartShow();
      invaderPart[c].move();
    }
    if (keyIsDown(LEFT_ARROW)) {
        ship.move(-1,0);
    }
    if (keyIsDown(RIGHT_ARROW)) {
      ship.move(1,0);
    }
    if (keyIsDown(UP_ARROW)) {
      ship.move(0,-1);
    }
    for (var o = playerPart.length-1; o >= 0; o--) {
      if (playerPart[o].deleteparticle) {
        playerPart.splice(o, 1);
      }
    }
    for (var a = invaderPart.length-1; a >= 0; a--) {
      if (invaderPart[a].deleteparticle) {
        invaderPart.splice(a, 1);
      }
    }
  }
  /* ------------------------------------------------------------------------ */
  //GameState is paused
  //game is now not updating
  else if (gameState === STATE_PAUSED) {
    pausescreenimg.style.display = 'inline';
    pausescreen.style.display = 'inline';

    ispaused = true;
    if (!buttonUnpause) {
      buttonUnpause = createButton('Resume');
      buttonUnpause.position(width - 127,25);
      buttonUnpause.mousePressed(changetopause);
      buttonUnpause.id('buttonUnpause');
    }
  }
  else if (gameState === STATE_GAME_OVER) {
    highscoreValue = Number(localStorage.getItem('highscoreValue'));
    if (score > highscoreValue) {
      localStorage.setItem('highscoreValue', score);
    }
    if (buttonpause) {
      buttonpause.remove();
      buttonpause = undefined;
    }
    gameoverscreen();
  }
  else if (gameState === STATE_HIGHSCORE) {
    highscoretest = loadImage('Images/highscore.jpg');
    background(highscoretest);
    highscoreNewGame = document.getElementById('newgameButton');
    highscoreNewGame.style.left = width - 187 + 'px';
    highscoreNewGame.style.top = 25 +'px';
    highscoreNewGame.style.height = 45 + 'px';
    highscoreNewGame.style.width = '150px';
    changetoHighscore();
    highscoretext();

    }
}

function keyPressed() {
  if (!(ship.doubleshoot)) {
    if (keyCode === 32 && ship.allowshoot === true) {
      var particle = new Particle(ship.x - 7.5, height - 48, -3.5);
      playerPart.push(particle);
      ship.allowshoot = false;
    }
  } else if (keyCode === 32 && ship.allowshoot === true) {
      var particleA = new Particle(ship.x - 15, height - 48, -3.5);
      var particleB = new Particle(ship.x, height - 48, -3.5);
      playerPart.push(particleA);
      playerPart.push(particleB);
      ship.allowshoot = false;
  }
}

function createinvaders() {
  if (!(level == bosslevels)) {
    number = startinv + level;
    if (nYval < 1) {
      nYval = 20;
    }

    for (var i = 0; i < number; i++) {
      if (b == 11) {
        b = 0;
        nYval = nYval - 35;
      }
      if (invaders.length <= number) {
        invaders.push(new Invader(b * 65 + 25, 0, nYval, undefined, 1));
        console.log('created one invader');
        b += 1;
        console.log('b = ' + b);
      }
    }
  } //else if (level === bosslevels){
    else {
    var boss = new Invader(width/2, 0, 150, 12.5, 5, img[6]);
    invaders.push(boss);
  }
}

function Ship() {
  this.allowshoot = false;
  this.doubleshoot = false;
  this.x = width/2;

  this.show = function() {
    image(img[5], this.x - 20, height-60, 40, 60);
  };
  this.move = function(val, powerboost) {
    if (powerboost) {
      powerboost = powerboost * 0.5;
      this.x += powerboost;
    } else {
      val = val * 5;
      this.x += val;
    }
  };
}

function PowerUp() {
  this.x = random(width);
  this.y = random(height/2);
  this.xspeed = 3.5;
  this.edgeR = false;
  this.edgeL = false;
  this.okey = true;

  this.show = function() {
    fill(255,0,0);
    image(img[4], this.x, this.y, 20, 20);
  };

  this.powerupChange = function() {
    if (this.okey === false) {
      this.okey = true;
    }
  };

  this.move = function() {
    this.x = this.x + this.xspeed;
  };

  this.check = function() {
    if (this.x > width) {
      this.edgeR = true;
    } else if (this.x < 0) {
      this.edgeL = true;
    }
  };

  this.shift = function() {
    if (this.edgeR) {
      this.xspeed = -this.xspeed;
      this.edgeR = false;
    } else if (this.edgeL) {
      this.xspeed = -this.xspeed;
      this.edgeL = false;
    }
};
}

function Invader(x, nDir, y, r, lifes, pic) {
  this.x = x;
  this.y = y || 150;
  this.r = r || 10;
  this.lifes = lifes;
  this.xDir = 2;
  this.nDir = nDir || undefined;
  this.edgeR = false;
  this.pic = pic || img[3];
  this.edgeL = false;


  this.show = function() {
    image(this.pic, this.x - 17.5, this.y, this.r*4, this.r*4);
  };

  this.move = function() {
    if (bosslevels == level) {
      this.x = this.x + this.xDir*2;
    }
    else {
      this.x = this.x + this.xDir
    }
  };

  this.swapcheck = function() {
    for (var i = 0; i < invaders.length; i++) {
      if (invaders[i].x > width) {
        this.edgeR = true;
      } else if (invaders[i].x < 0) {
        this.edgeL = true;
      }
    }
  };

  this.shift = function() {
    if (this.edgeR) {
      this.xDir = -2;
      this.y += this.r;
      this.edgeR = false;
    } else if (this.edgeL) {
      this.xDir = 2;
      this.y += this.r;
      this.edgeL = false;
    }
  };
}

function Particle(x,y, nDir) {
  this.x = x;
  this.y = y;
  this.r = 8;
  this.deleteparticle = false;
  this.nDir = nDir;

  this.hit = function(x,y) {
    var d = dist(this.x, this.y, x, y);
    if (d <= this.r *2.5) {
      return true;
    } else {
      return false;
   }
};

  this.playerPartShow = function() {
    fill(150, 0, 250);
    image(img[1], this.x ,this.y , this.r*2, this.r*2);
  };

  this.invaderPartShow = function() {
    fill(150, 0, 250);
    image(img[2], this.x ,this.y , this.r*2, this.r*2);
  };

  this.particleDelete = function() {
    this.deleteparticle = true;
  };

  this.move = function() {
      this.y += nDir;
  };
}
