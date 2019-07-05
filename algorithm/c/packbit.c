/*  RERFENCE https://blog.csdn.net/sdfdsh/article/details/8190596
**
**
*/

// Assuming compressor logic is maximally efficient,
// worst case input with no duplicate runs of 3 or more bytes
// will be compressed into a series of verbatim runs no longer
// than 128 bytes, each preceded by length byte.
// i.e. worst case output length is not more than 129*ceil(n/128)
// or slightly tighter, 129*floor(n/128) + 1 + (n%128)

unsigned int packbits(unsigned char *src, unsigned char *dst, unsigned int n){
    unsigned char *p, *q, *run, *dataend;
    int count, maxrun;
 
    dataend = src + n;
    for( run = src, q = dst; n > 0; run = p, n -= count ){
        // A run cannot be longer than 128 bytes.
        maxrun = n < 128 ? n : 128;
        if(run <= (dataend-3) && run[1] == run[0] && run[2] == run[0]){
            // 'run' points to at least three duplicated values.
            // Step forward until run length limit, end of input,
            // or a non matching byte:
            for( p = run+3; p < (run+maxrun) && *p == run[0]; )
                ++p;
            count = p - run;
 
            // replace this run in output with two bytes:
            *q++ = 1+256-count; /* flag byte, which encodes count (129..254) */
 
            *q++ = run[0];      /* byte value that is duplicated */
 
        }else{
            // If the input doesn't begin with at least 3 duplicated values,
            // then copy the input block, up to the run length limit,
            // end of input, or until we see three duplicated values:
            for( p = run; p < (run+maxrun); )
                if(p <= (dataend-3) && p[1] == p[0] && p[2] == p[0])
                    break; // 3 bytes repeated end verbatim run
                else
                    ++p;
            count = p - run;
            *q++ = count-1;        /* flag byte, which encodes count (0..127) */
            memcpy(q, run, count); /* followed by the bytes in the run */
            q += count;
        }
    }
    return q - dst;
}


unsigned int unpackbits(unsigned char *outp, unsigned char *inp,
            unsigned int outlen, unsigned int inlen)
{
    unsigned int i, len;
    int val;
 
    /* i counts output bytes; outlen = expected output size */
    for(i = 0; inlen > 1 && i < outlen;){
        /* get flag byte */
        len = *inp++;
        --inlen;
 
        if(len == 128) /* ignore this flag value */
            ; // warn_msg("RLE flag byte=128 ignored");
        else{
            if(len > 128){
                len = 1+256-len;
 
                /* get value to repeat */
                val = *inp++;
                --inlen;
 
                if((i+len) <= outlen)
                    memset(outp, val, len);
                else{
                    memset(outp, val, outlen-i); // fill enough to complete row
                    printf("unpacked RLE data would overflow row (run)\n");
                    len = 0; // effectively ignore this run, probably corrupt flag byte
                }
            }else{
                ++len;
                if((i+len) <= outlen){
                    if(len > inlen)
                        break; // abort - ran out of input data
                    /* copy verbatim run */
                    memcpy(outp, inp, len);
                    inp += len;
                    inlen -= len;
                }else{
                    memcpy(outp, inp, outlen-i); // copy enough to complete row
                    printf("unpacked RLE data would overflow row (copy)\n");
                    len = 0; // effectively ignore
                }
            }
            outp += len;
            i += len;
        }
    }
    if(i < outlen)
        printf("not enough RLE data for row\n");
    return i;
}
