'use strict'

const test = require('tap').test
const path = require('path')
const devDir = require('./common').devDir()
const nnabt = require('../lib/node-nnabt')
const requireInject = require('require-inject')
const configure = requireInject('../lib/configure', {
  'graceful-fs': {
    openSync: function () { return 0 },
    closeSync: function () { },
    writeFile: function (file, data, cb) { cb() },
    stat: function (file, cb) { cb(null, {}) },
    mkdir: function (dir, options, cb) { cb() }
  }
})

const EXPECTED_PYPATH = path.join(__dirname, '..', 'nnabt', 'pylib')
const SEPARATOR = process.platform === 'win32' ? ';' : ':'
const SPAWN_RESULT = { on: function () { } }

require('npmlog').level = 'warn'

test('configure PYTHONPATH with no existing env', function (t) {
  t.plan(1)

  delete process.env.PYTHONPATH

  var prog = nnabt()
  prog.parseArgv([])
  prog.spawn = function () {
    t.equal(process.env.PYTHONPATH, EXPECTED_PYPATH)
    return SPAWN_RESULT
  }
  prog.devDir = devDir
  configure(prog, [], t.fail)
})

test('configure PYTHONPATH with existing env of one dir', function (t) {
  t.plan(2)

  var existingPath = path.join('a', 'b')
  process.env.PYTHONPATH = existingPath

  var prog = nnabt()
  prog.parseArgv([])
  prog.spawn = function () {
    t.equal(process.env.PYTHONPATH, [EXPECTED_PYPATH, existingPath].join(SEPARATOR))

    var dirs = process.env.PYTHONPATH.split(SEPARATOR)
    t.deepEqual(dirs, [EXPECTED_PYPATH, existingPath])

    return SPAWN_RESULT
  }
  prog.devDir = devDir
  configure(prog, [], t.fail)
})

test('configure PYTHONPATH with existing env of multiple dirs', function (t) {
  t.plan(2)

  var pythonDir1 = path.join('a', 'b')
  var pythonDir2 = path.join('b', 'c')
  var existingPath = [pythonDir1, pythonDir2].join(SEPARATOR)
  process.env.PYTHONPATH = existingPath

  var prog = nnabt()
  prog.parseArgv([])
  prog.spawn = function () {
    t.equal(process.env.PYTHONPATH, [EXPECTED_PYPATH, existingPath].join(SEPARATOR))

    var dirs = process.env.PYTHONPATH.split(SEPARATOR)
    t.deepEqual(dirs, [EXPECTED_PYPATH, pythonDir1, pythonDir2])

    return SPAWN_RESULT
  }
  prog.devDir = devDir
  configure(prog, [], t.fail)
})
