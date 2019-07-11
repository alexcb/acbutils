# acbutils
misc python utilities

    sudo pip3 install git+git://github.com/alexcb/acbutils.git@master

or from local copy:

    sudo pip3 install .



## structured_stream

example of reading binary from stdin

    # run with
    cat /tmp/data.scratch | python3 scratch-decoder.py

    # scratch-decoder.py
    import sys
    from acbutils.structured_stream import StructuredStream

    ss = StructuredStream(sys.stdin.buffer)
    header = ss.get_bytes(64)
    print(header)

    
