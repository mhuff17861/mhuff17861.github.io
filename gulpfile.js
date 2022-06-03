//import needed plugins
const gulp = require('gulp');
const sass = require('gulp-sass')(require('sass'));
const clean = require('gulp-clean')

//Define pathnames
const sassSrc = 'scss/core.scss'
const sassInc = [ 'node_modules/bootstrap/scss' ]
const sassDevDest = 'portfoliosite/static/css'
const sassDest = '/var/www/micah-huff.com/static/css'
const jsSrc = [ 'node_modules/bootstrap/dist/js/bootstrap.min.js' ]
const jsDevDest = 'portfoliosite/static/js'
const jsDest = '/var/www/micah-huff.com/static/js'

function cleanBuild() {
  return gulp.src([sassDest + "/*", jsDest + "/*"])
          .pipe(clean())
}

function devTranspileSass() {
        return gulp.src(sassSrc)
                .pipe(sass({
                        includePaths: sassInc
                }).on('error', sass.logError))
                .pipe(gulp.dest(sassDevDest))
}

function devJS() {
        return gulp.src(jsSrc)
                .pipe(gulp.dest(jsDevDest))
}

function transpileSass() {
        return gulp.src(sassSrc)
                .pipe(sass({
                        includePaths: sassInc
                }).on('error', sass.logError))
                .pipe(gulp.dest(sassDest))
}

function js() {
        return gulp.src(jsSrc)
                .pipe(gulp.dest(jsDest))
}


function defaultTask(cb) {
  // place code for your default task here
        devTranspileSass();
        devJS();
        cb();
}

exports.cleanBuild = cleanBuild
exports.transpileSass = transpileSass
exports.devTranspileSass = devTranspileSass
exports.js = js
exports.devJS = devJS
exports.devSetup = gulp.parallel(devTranspileSass, devJS)
exports.prodSetup = gulp.parallel(transpileSass, js)
exports.default = defaultTask
