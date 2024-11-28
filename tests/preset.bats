#!/usr/bin/env bash

setup() {
    bats_load_library bats-assert
    bats_load_library bats-file
    bats_load_library bats-support

    if [ -f /usr/local/bin/getansible.sh ]; then
        chmod +x /usr/local/bin/getansible.sh
    fi

    if [ -n "$TMPDIR" ]; then
      export TMPDIR="$TMPDIR/bats"
    else
      export TMPDIR="/tmp/bats"
    fi
    mkdir -p $TMPDIR
}

assert_teardown() {
    run test -z "$(ls -A $TMPDIR | grep -v 'bats-')"
    assert_success
}

# bats test_tags=T001
@test "T001: getansible.sh" {
    run preset
    assert_failure 1
    assert_output --partial "Usage: preset"
    assert_teardown
}