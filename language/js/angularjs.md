## Angularjs

## Introduction

Angularjs helps to connect javascript and html document component in an interactive way.

<ng>-<html tag attr> api can just replace noraml <html tag attr>
with javascript #scope function.

[More tutorials](https://www.w3schools.com/angular/)

## module linkage

[dynamic linkage](https://docs.angularjs.org/misc/downloading)
```html
<!doctype html>
<html ng-app>
  <head>
    <title>My AngularJS App</title>
    <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.5.6/angular.min.js"></script>
  </head>
  <body>
  </body>
</html>
```
[src download](https://code.angularjs.org/)

## api

1. ng-app
2. ng-controller
3. ng-repeat
4. ng-hide
5. ng-change
6. ng-model
7. ng-disabled
8. ng-cloak


```html
<!DOCTYPE html>
<html ng-app="HC_App" ng-controller="HC_Ctrl">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <script src="../js/angular.min.js"></script>
        <title>Demo</title>
    </head>
    <style>
        .navbar {
          margin-bottom: 0;
          border-radius: 0;
        }
        .row.content {height: 450px}
        .sidenav {
          padding-top: 20px;
          background-color: #f1f1f1;
          height: 100%;
        }
            tr{
            height: 50px;
        }
    <body>
        <div class="container-fluid text-center" ng-cloak>
            <div class="row content">
                <div class="col-sm-2 sidenav">
                    <p ng-repeat="x in Menu" ng-hide="x.hide"><a target="_self" href="{{x.href}}">{{x.txt}}</a></p>
                </div>
                <div class="col-sm-8 text-left">
                    <nav class="navbar navbar-default">
                        <div class="container-fluid">
                            <nav aria-label="Page navigation example">
                                <ul class="pagination">
                                    <li ng-repeat="x in MenuB" class="{{x.page_item}}" >
                                    <a class="page-link" target="_self" href="{{x.href}}">{{x.txt}}</a>
                                    </li>
                                </ul>
                            </nav>
                        </div>
                    </nav>
                    <div>
                        <div class="panel panel-default">
                            <div class="panel-heading"></div>
                            <div class="panel-body"></div>
                        <table>
                                <tr>
                                    <td> <input type="checkbox" ng-model="model.enabled" />enabled</td>
                                </tr>
                                <tr>
                                    <td> <input type="number" ng-model="model.number" min="0" max="9999" ng-disabled="model.enabled==0"/></td>
                                    <td> <input type="range" ng-model="model.number" min="0" max="9999" ng-disabled="model.enabled==0"/></td>
                                </tr>
            </div>  

        </div>
    </body>
    <script>
        var Menu = [
        {'txt':'itemA','href':'A.html','page_item':'page-item-active'},
        {'txt':'itemB','href':'B.html','page_item':'page-item'},
        {'txt':'itemC','href':'C.html','page_item':'page-item'}];

        var MenuB = [
        {'txt':'itemA','href':'A.html','page_item':'page-item-active'},
        {'txt':'itemB','href':'B.html','page_item':'page-item'},
        {'txt':'itemC','href':'C.html','page_item':'page-item'}];

        var app = angular.module('HC_App', []);

        app.config(['$httpProvider', function($httpProvider) {
            //initialize get if not there
            if (!$httpProvider.defaults.headers.get) {
                $httpProvider.defaults.headers.get = {};
            }    
            // Answer edited to include suggestions from comments
            // because previous version of code introduced browser-related errors

            //disable IE ajax request caching
            $httpProvider.defaults.headers.get['If-Modified-Since'] = 'Mon, 26 Jul 1997 05:00:00 GMT';
            // extra
            $httpProvider.defaults.headers.get['Cache-Control'] = 'no-cache';
            $httpProvider.defaults.headers.get['Pragma'] = 'no-cache';
        }]);
        app.config(['$locationProvider', function($locationProvider) {
        	// $locationProvider.html5Mode(true);
        	$locationProvider.html5Mode({
        		enabled: true,
        		requireBase: false,
        			});
        }]);
        app.controller('HC_Ctrl', ['$scope', '$location','$http', function($scope,$location, $http) {
                $scope.model = {
                    "enabled":0,
                    "number": 1
                }
        }
    </script>
</html>
```