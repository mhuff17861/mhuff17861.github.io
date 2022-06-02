//import needed plugins
const gulp = require('gulp');
const sass = require('gulp-sass')(require('sass'));
const clean = require('gulp-clean')

//Define pathnames
const sassSrc = 'scss/core.scss'
const sassDest = 'portfoliosite/static/css'
const sassInc = [ 'node_modules/bootstrap/scss' ]
const jsSrc = [ 'node_modules/bootstrap/dist/js/bootstrap.min.js' ]
const jsDest = 'portfoliosite/static/js'

function cleanBuild() {
  return gulp.src([sassDest + "/*", jsDest + "/*"])
          .pipe(clean())
}

function transpileSass() {
        return gulp.src(sassSrc)
                .pipe(sass({
                        includePaths: sassInc
                }).on('error', sass.logError))
                .pipe(gulp.dest(sassDest))
}

function devJS() {
        return gulp.src(jsSrc)
                .pipe(gulp.dest(jsDest))
}

function defaultTask(cb) {
  // place code for your default task here
        transpileSass();
        devJS();
        cb();
}

exports.cleanBuild = cleanBuild
exports.transpileSass = transpileSass
exports.devJS = devJS
exports.devSetup = gulp.parallel(transpileSass, devJS)
exports.default = defaultTask
