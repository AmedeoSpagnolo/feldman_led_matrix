var gulp = require('gulp'),
   shell = require('gulp-shell'),
   watch = require('gulp-watch');

gulp.task('default', function () {
    return watch(['scripts/main.py'])
        .pipe(shell(['./update']));
});
