//import needed plugins
const gulp = require('gulp');
const sass = require('gulp-sass')(require('sass'));
const clean = require('gulp-clean')

//Define pathnames
const sassSrc = 'scss/core.scss'
const sassInc = [ 'node_modules/bootstrap/scss' ]
const sassDevDest = 'portfoliosite/static/css'
const sassDest = '/var/www/micah-huff.com/static/css'
const bootstrapJSSrc = [ 'node_modules/bootstrap/dist/js/bootstrap.min.js' ]
const bootstrapJSDevDest = 'portfoliosite/static/js'
const bootstrapJSDest = '/var/www/micah-huff.com/static/js'
const howlerJSSrc = [ 'node_modules/howler/dist/howler.min.js' ]
const howlerJSDevDest = 'portfoliosite/portfolio_music_player/static/portfolio_music_player/js'
const howlerJSDest = '/var/www/micah-huff.com/portfolio_music_player/static/portfolio_music_player/js'

function cleanDevBuild() {
  return gulp.src([sassDevDest + "/*", bootstrapJSDevDest + "/*"])
          .pipe(clean());
}

function cleanBuild() {
  return gulp.src([sassDest + "/*", bootstrapJSDest + "/*"])
          .pipe(clean());
}

function devTranspileSass() {
  return gulp.src(sassSrc)
          .pipe(sass({
                  includePaths: sassInc
          }).on('error', sass.logError))
          .pipe(gulp.dest(sassDevDest));
}

function devBootstrapJS() {
        return gulp.src(bootstrapJSSrc)
                .pipe(gulp.dest(bootstrapJSDevDest));
}

function devHowlerJS() {
  return gulp.src(howlerJSSrc)
          .pipe(gulp.dest(howlerJSDevDest));
}

function devJS() {
  devBootstrapJS();
  devHowlerJS();
}

function transpileSass() {
  return gulp.src(sassSrc)
          .pipe(sass({
                  includePaths: sassInc
          }).on('error', sass.logError))
          .pipe(gulp.dest(sassDest));
}

function bootstrapJS() {
  return gulp.src(bootstrapJSSrc)
          .pipe(gulp.dest(bootstrapJSDest))
}

function howlerJS() {
  return gulp.src(howlerJSSrc)
    .pipe(gulp.dest(howlerJSDest));
}

function prodJS() {
  bugootstrapJS();
  howlerJS();
}

function defaultTask(cb) {
  devTranspileSass();
  devJS();
  cb();
}

exports.cleanBuild = cleanBuild
exports.cleanDevBuild = cleanDevBuild
exports.transpileSass = transpileSass
exports.devTranspileSass = devTranspileSass
exports.prodJS = prodJS
exports.devJS = devJS
exports.devSetup = gulp.parallel(devTranspileSass, devJS)
exports.prodSetup = gulp.parallel(transpileSass, prodJS)
exports.default = defaultTask
