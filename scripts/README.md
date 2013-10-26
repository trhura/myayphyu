How to run
==========

```bash
$ ./gentxtfiles.rb && \
        ./txt2png.rb *.txt && \
        for image in *.png; do convert "$image" -trim -strip "$image";done && \
        for f in *.png; do mv $f "char$f";done

$ mv *.png ../res/drawable-hdpi/
```
