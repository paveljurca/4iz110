#!/usr/bin/perl -T

# Taint mode
# perlrun PERL5OPT=-T

use strict;
use warnings;
use LWP::UserAgent;

# ==================
my $dotaz   = sestav_dotaz(
    #ref eq 'HASH'
    zpracuj(nacti())
);
my $odpoved = posli_dotaz($dotaz);

relace_dump();
# ==================

#nacti data z formulare
sub nacti {
    read(STDIN, my $q, $ENV{CONTENT_LENGTH})
        or die('zadna data');

    return $q;
}
#zpracuj obsah formulare
sub zpracuj {
    my %f;
    foreach (split /&/, shift) {
        #obsah POST <input type="hidden" name="data">
        unless (/^data/) {
            #dekoduj mezery
            tr/+/ /;
            #dekoduj znaky
            s/%([a-f0-9][a-f0-9])/chr(hex($1))/egi;
            #orizni mezery
            s/^\s+|\s+$//g;
        }
        #parametr=hodnota (URL)
        m/^([^=]+)=(.+)$/;
        $f{$1} = $2;
    }

    return \%f;
}
#sestav parametry HTTP dotazu
sub sestav_dotaz {
    my(%f, $d) = %{ shift @_ };
    $d = HTTP::Request->new(
        $f{method}  => $f{url}
    );
    #pridej k dotazu telo, pokud POST
    $d->content($f{data})
        if $f{method} =~ /POST/i;
    #Referer
    $d->push_header(Referer => $f{referer})
        if exists $f{referer};
    #User-Agent
    $d->push_header(User_Agent => $f{ua})
        if exists $f{ua};

    #HTTP version
    #TODO: $d->version($f{version});

    return $d;
}
#posli dotaz a vrat odpoved
sub posli_dotaz {
    my $ua = LWP::UserAgent->new;

    return $ua->request(shift);
}
#vypis vysledek HTTP relace
sub relace_dump {
    printf(
        "%s\n\n%s\n=====\n\n%s",
        'Content-Type: text/plain; charset=utf-8',
        $dotaz->as_string,
        #pokud chyba, zobraz info
        $odpoved->code != 500 ?
            $odpoved->as_string : $odpoved->status_line
    );
}
