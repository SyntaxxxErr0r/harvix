#!/usr/bin/perl

# this code written by David Skrenta CEO of Harvix Search May 2013 (C) comments vary throughout the file
# call specilized perl modules

use strict;
use JSON;
use URI::Fetch;
#use Data::Dumper;
#use WebService::Blekko;
use Encode;
use XML::Simple;

my %escapes;
setup_escapes();

print "Content-type: text/html\n\n";

my $query = parse_query();

print_header($query);

#7search ad stuff

my $affiliate   = '78752';
my $token       = 'A814D87FA1154101A8FCC76E8DC915A3';
my $rid         = 'harvix.com';
my $qu          = urlencode($query);
my $ip_address  = $ENV{ 'REMOTE_ADDR' };
my $fwd         = urlencode( $ENV{ 'HTTP_X_FORWARDED_FOR' } );
my $st          = 'typein';     # typein, link, context
my $page_url    = urlencode( 'http://' . $ENV{'SERVER_NAME'} . $ENV{'SCRIPT_NAME'} . $ENV{'QUERY_STRING'} );
my $ua          = urlencode( $ENV{ 'HTTP_USER_AGENT' } );
my $lang        = urlencode( $ENV{ 'HTTP_ACCEPT_LANGUAGE' } );
my $pn          = 1;        # page number
my $r           = 25;       # number of results requested; max is 25
my $filter      = 'yes';    # adult filter
my $mobile      = 'no';       # mobile device user
 
my $request =   'http://meta.7search.com/feed/xml.aspx?affiliate=' . $affiliate .
                '&token=' . $token .
                '&rid=' . $rid .
                '&qu=' . $qu .
                '&pn=' . $pn .
                '&r=' . $r .
                '&filter=' . $filter .
                '&ip_address=' . $ip_address .
                '&st=' . $st .
                '&page_url=' . $page_url .
                '&lang=' . $lang .
                '&mobile=' . $mobile .
                '&ua=' . $ua .
                '&x_forwarded_for=' . $fwd;


my $xml_page = URI::Fetch->fetch( $request );
my $xml_text = $xml_page->content();
my $xml = XMLin( $xml_text );

sub utf8_on
{
    my($str) = @_;

    if( $str )
    {
        String::Charset::utf8_clean( $str );

        Encode::_utf8_on($str);

        if(! Encode::is_utf8($str, 1) )
        {
            Encode::_utf8_off($str);
        }
    }

    return $str;
}

=head2 utf8_off($string)

Unconditionally marks a string as not UTF-8. If the string isn't
valid UTF-8, chaos is in your immediate future.

=cut

sub utf8_off
{
    my( $str ) = @_;

    if( $str )
    {
        Encode::_utf8_off($str);
    }

    return $str;
}

# CALL IZIK API

my $json_page = URI::Fetch->fetch("http://blekko.com/api/p1?q=$query&auth=c31c6fd0&add_slashtags=homework-help");
my $json_text = $json_page->content();
my $json = decode_json( $json_text );

# print Dumper($json), "\n";

if ( ! defined $json )
{
    print "no results\n";
    exit(0);
}

if ( ! defined $json->{tags} )
{
    print "no tags\n";
    exit(0);
}


# tags go into categories 


foreach my $tag ( @{ $json->{tags} } )
{
    my $category = $tag->{name};
    my $results = $tag->{results};

# print categories 

	if($category eq "ORIG")
	{
	#my $num = scalar @{ $results };
    	#print "<div id=\"count\"><span class=\"label\"><h5>$num results:</h5></span></div> <div id=\"upper\"><span class=\"label label-important\"><h5>Top Results:</h5></span></div><hr></hr>";
	}

	elsif($category eq "WIKI")
        {

	}

	elsif($category eq "NAV")
	{

	}
	
	elsif($category eq "STOCK")
        {
	}

        elsif($category eq "FANDANGO")
        {
	#print "<div id=\"upper\"><span class=\"label label-important\"><h5>Movies:</h5></span></div><hr></hr>";
        }

	elsif($category eq "IMAGE")
	{
	}

	elsif($category eq "date")
	{
	#my $num = scalar @{ $results };
        #print "<div id=\"count\"><span class=\"label\"><h5>$num results:</h5></span></div> <div id=\"upper\"><span class=\"label label-info\"><h5>Latest:</h5></span></div><hr></hr>";
	}
	
	elsif($category eq "PEOPLE")
        {
        #my $num = scalar @{ $results };
        #print "<div id=\"count\"><span class=\"label\"><h5>$num results:</h5></span></div> <div id=\"upper\"><span class=\"label label-info\"><h5>social:</h5></span></div><hr></hr>";
        }

	elsif($category eq "RETAIL")
	{

	}

	else
	{
	#my $num = scalar @{ $results };
        #print "<div id=\"count\"><span class=\"label\"><h5>$num results:</h5></span></div> <div id=\"upper\"><span class=\"label label-info\"><h5>$category:</h5></span></div><hr></hr>";
	}

# print results inside categories 

	if($category eq "NAV")
	{

	}	

	elsif($category eq "RETAIL")
	{

	}

	elsif($category eq "WIKI")
	{
		my $wiki_count = 1;

        	foreach my $result ( @{ $results } )
        	{
                	if($wiki_count == "1")
			{
				print"<div class=\"hero-unit-wiki\">";
				print" <ul id=\"myTab\" class=\"nav nav-tabs\">
              			<li class=\"active\"><a href=\"#instant\" data-toggle=\"tab\">Instant Information</a></li>
				<li><a href=\"#expand\" data-toggle=\"tab\">Expand</a></li>
              			<li><a href=\"#notes\" data-toggle=\"tab\">Notes</a></li>
            			</ul>";
				print"<div id=\"myTabContent\" class=\"tab-content\">
              			<div class=\"tab-pane fade in active\" id=\"instant\">";
				my $title = $result->{'t'};
                		my $url = $result->{'u'};
                		my $rurl = $result->{'du'};
                		my $snippet = $result->{'ws'};
				my $img = $result->{'wi'};
				print"<table cellpadding=\"10\"><tr><td>";
				print"<a href=\"#\" data-toggle=\"modal\"><img src=\"$img\"/ class=\"img-rounded\"></a></td><td>";
                		print"<h3><span style=\"black\">$title</span></h3>";
				print"$snippet";
                		print"<p><span style=\"color:green\">$rurl</span>";
				print"</td>";
                                print"<td><iframe src=\"http://harvix.com/wolf.cgi?$query\" width=\"500px\" height=\"300px\" frameborder=\"0\"></iframe></td>";
				print"</tr></table>";
				print"</div>";
				print"<div class=\"tab-pane fade\" id=\"expand\">";
                                print"<iframe src=\"$url\" width=\"100%\" height=\"600px\" frameborder=\"0\"></iframe>";
                                print"</div>";
				print"<div class=\"tab-pane fade\" id=\"notes\">";
				print"<div id=\"frame4\"></div>";
				print"</div>";
				print"</div></div>";
			}

			else 
			{

			}
		
			$wiki_count ++;
		}

	}


	elsif($category eq "STOCK")
	{
	}

	elsif($category eq "FANDANGO")
	{
		print"<div class=\"panel panel-danger\"><div class=\"panel-heading\"><h3 class=\"panel-title\">MOVIES</h3></div><div class=\"panel-body\">";	
	
		foreach my $result ( @{ $results } )
                {
			my $fandango = $result->{'fandango'};
			my $movie = $fandango->{'movie'};
			my $snippet = $movie->{'snippet'};
			my $poster = $movie->{'poster'};
			my $title = $movie->{'title'};
			my $rating = $movie->{'rating'};
			my $release_date = $movie->{'release_date'};
			my $runtime = $movie->{'runtime'};
			my $trailer_url = $movie->{'trailer_url'};
			my $fan_url = $movie->{'url'};
			print"<div class=\"hero-unit-wiki\">";
			print"<table cellpadding=\"10\"><tr><td>";
                        print"<a href=\"#myModalwiki\" data-toggle=\"modal\"><img src=\"$poster\"/ class=\"img-rounded\"></a></td><td>";
                        print"<a href=\"#myModalwiki\" data-toggle=\"modal\"><h3><span style=\"black\">$title</span></h3></a>";
                        print"Rating: $rating<br>";
			print"Released: $release_date<br>";
			print"Runtime: $runtime minutes<br>";
			print"$snippet<br>";
			print"<a href=\"$trailer_url\"><span style=\"color:#195189;\">Watch Trailer</span></a> &middot; <a href=\"$fan_url\"><span style=\"color:#195189;\">Get Tickets & Showtimes</span></a>";
                        print"<p></td></tr></table>";
			print"</div>";
		}
		print"</div></div>";
	}	

	elsif($category eq "PEOPLE")
	{

	print"<div class=\"panel panel-primary\"><div class=\"panel-heading\"><h3 class=\"panel-title\">SOCIAL</h3></div><div class=\"panel-body\">";
	
	print"<div id=\"scrollable\"><div id=\"items\">";

        foreach my $result ( @{ $results } )
        {
                print"<div class=\"item2\">";
                print"<div class=\"hero-unit-spec\">";
                my $title = $result->{'t'};
                my $url = $result->{'u'};
		my $snippet = $result->{'s'};
                $snippet =~ s/<\/?(b|strong)>//g;
                if ( length($snippet) > 150 )
                {
                        $snippet = substr($snippet, 0, 150);
                        $snippet =~ s/\s[^\s]*$//;
                        $snippet .= ' ...';
                }
                print"<a href=\"$url\"><span style=\"color:#195189;\"><h4>$title</h4></span></a>";
                print"$snippet";
                print"<p><span style=\"color:green\">$url</span>";
                print"</div></div>";
                #print"<hr></hr><p>";
                #print Dumper($result);
        }

        print"</div></div></div></div>";

    print "<p>\n";

        }
	
	elsif($category eq "ORIG")
	{

	print"<div class=\"panel panel-success\"><div class=\"panel-heading\"><h3 class=\"panel-title\">TOP RESULTS</h3></div><div class=\"panel-body\">";
	print"<div id=\"scrollable\"><div id=\"items\">";

	my $count = 0;
	my $boxcount = 0;
	
	foreach my $result ( @{ $results } )
        {
                 print"<div class=\"item2\">";
        	 if ($boxcount == 0)
		 {        
		 	print"<div class=\"hero-unit-spec-ad\">";
        	 }
		 else
		 {
		 	print"<div class=\"hero-unit-spec\">";	
		 }
	         my $title = $result->{'t'};
                 my $url = $result->{'u'};
                 my $rurl = $result->{'du'};
                 my $snippet = $result->{'s'};
                 $snippet =~ s/<\/?(b|strong)>//g;
                 if ( length($snippet) > 150 )
                 {
                 	$snippet = substr($snippet, 0, 150);
                        $snippet =~ s/\s[^\s]*$//;
                        $snippet .= ' ...';
                 }

		if ($count == 0)
                {
			my $countfun = 0;
			#print"<div class=\"hero-unit-spec-ad\">";			
 		
			if ( defined $xml && defined $xml->{'SITE'} )
			{
    				foreach my $ad ( @{ $xml->{'SITE'} } )           
    				{
        				if ($countfun == 0)
        				{
                				print "<a href=\"$ad->{'URL'}\"><span style=\"color:#195189;\"><h4>$ad->{'NAME'}</h4></span></a><p>$ad->{'DESCRIPTION'}<p><span style=\"color:green\">$ad->{'HTTPLINK'}</span><small><p>Ad-$query</small>\n";
        				}
        
        				else {}
        				$countfun++;
    				}
				#print"<div>";
			}
		

		}
		
		else
		{
		 	print"<a href=\"$url\"><span style=\"color:#195189;\"><h4>$title</h4></span></a>";
                        print"$snippet";
                        print"<p><span style=\"color:green\">$rurl</span>";
		}

		print"</div></div>";
		$count++;
		$boxcount++;
	}

        print"</div></div>";
	print"</div></div>";
    	print "<p>\n";

	print"<iframe src=\"http://harvix.com/facts4.cgi?$query\" width=\"100%\" height=\"350px\" frameborder=\"0\"></iframe>";

	}

	elsif($category eq "IMAGE")
        {
                print"<div class=\"panel panel-danger\"><div class=\"panel-heading\"><h3 class=\"panel-title\">IMAGES</h3></div><div class=\"panel-body\">";

		print"<div id=\"scrollable\"><div id=\"items\">";

                foreach my $result ( @{ $results } )
                {
                        print"<div class=\"item\">";
                        my $url = $result->{'u'};
                        print"<a href=\"$url\" target=\"_blank\"><img src=\"$url\" height=\"280px\" alt=\"\" onerror=\"this.style.display=\'none\'\"></a>";
			print"</div>";
                }

                print"</div></div></div></div>";
        }



	else
	{

	print"<div class=\"panel panel-primary\"><div class=\"panel-heading\"><h3 class=\"panel-title\"><div id=\"upper\">$category</div></h3></div><div class=\"panel-body\">";

	print"<div id=\"scrollable\"><div id=\"items\">";    
	
	foreach my $result ( @{ $results } )
    	{
		print"<div class=\"item2\">";
                print"<div class=\"hero-unit-spec\">";
		my $title = $result->{'t'};
                my $url = $result->{'u'};
		my $rurl = $result->{'du'};
                my $snippet = $result->{'s'};
                $snippet =~ s/<\/?(b|strong)>//g;
        	if ( length($snippet) > 150 )
        	{
                	$snippet = substr($snippet, 0, 150);
                	$snippet =~ s/\s[^\s]*$//;
                	$snippet .= ' ...';
        	}
		print"<a href=\"$url\"><span style=\"color:#195189;\"><h4>$title</h4></span></a>";
		print"$snippet";
                print"<p><span style=\"color:green\">$rurl</span>";
                print"</div></div>";
		#print"<hr></hr><p>";
                #print Dumper($result);
        }
	
	print"</div></div></div></div>";

    print "<p>\n";
	}

}

# print footer HTML


print_footer();


# define subroutines 

sub setup_escapes
{
	for (0..255)
	{
	    $escapes{chr($_)} = sprintf("%%%02X", $_);
	}
	$escapes{' '} = '+';
}

sub urlencode
{
    my $url = shift;

    $url =~ s/([^A-Za-z0-9\-_.!~*\'()])/$escapes{$1}/ge if defined $url;
    return $url;
}

sub urldecode
{
    my $url = shift;

    $url =~ tr/+/ / if defined $url;
    $url =~ s/%([0-9A-Fa-f]{2})/chr(hex($1))/eg if defined $url;

    return $url;
}

sub parse_query
{
	my $query = $ENV{QUERY_STRING} || shift || 1;

	$query =~ s/q=//;
	$query = urldecode($query);
	#$query =~ s/\+/ /g;
	$query =~ s/[\[\]\(\)\.\?]/ /g;
	$query =~ s/^\s*//;
	$query =~ s/\s*$//;
	$query =~ s/\s+/ /g;
	
	return $query;
}





sub print_header
{
	my ( $query ) = @_;

	$query =~ s/[<>\&]//g;

print <<EOF





<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>$query - Harvix</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- Le styles -->
    <link href="bootstrap.css" rel="stylesheet">
    
<style>iframe { border: none; }</style>

	<style type="text/css">
      body {
	padding-top: 60px;
        padding-bottom: 40px;

      }



	  #scrollable {
       overflow: auto;
       width:100%;
       height:294px; 
    }


   #scrollable-img {
       overflow: auto;
       width:100%;
       height:300px; 
    }


   #items {
     width: 100000px; /* itemWidth x itemCount */
    }

  .item{
     float:left;      
  }

  .item2{
	width:400px;
	height:200px;
     float:left;      
  }

 .item3{
        width:350px;
        height:220px;
     float:left;      
  }

.itemfacts{
        width:300px;
        height:200px;
     float:left;      
  }

 .itemwiki{
     width:100%;
     float:left;      
  }


.hero-unit-spec {
  padding: 10px;
  margin-bottom: 30px;
  height:200px;
  font-size: 14px;
  font-weight: 200;
  line-height: 30px;
  color: inherit;
  background-color: white;
  -webkit-border-radius: 6px;
     -moz-border-radius: 6px;
          border-radius: 6px;
        overflow:hidden;
}

.hero-unit-spec-ad {
  padding: 10px;
  margin-bottom: 30px;
  height:200px;
  font-size: 14px;
  font-weight: 200;
  line-height: 30px;
  color: inherit;
  background-color: #f9fcf7;
  -webkit-border-radius: 6px;
     -moz-border-radius: 6px;
          border-radius: 6px;
        overflow:hidden;
}

#count{
     float:right;      
}

#upper{
text-transform:uppercase;
}

.panel {
  margin-bottom: 20px;
  background-color: #ffffff;
  border: 1px solid transparent;
  border-radius: 4px;
  -webkit-box-shadow: 0 1px 1px rgba(0, 0, 0, 0.05);
          box-shadow: 0 1px 1px rgba(0, 0, 0, 0.05);
}

.panel-body {
  padding: 15px;
}

.panel-body:before,
.panel-body:after {
  display: table;
  content: " ";
}

.panel-body:after {
  clear: both;
}

.panel-body:before,
.panel-body:after {
  display: table;
  content: " ";
}

.panel-body:after {
  clear: both;
}

.panel > .list-group {
  margin-bottom: 0;
}

.panel > .list-group .list-group-item {
  border-width: 1px 0;
}

.panel > .list-group .list-group-item:first-child {
  border-top-right-radius: 0;
  border-top-left-radius: 0;
}

.panel > .list-group .list-group-item:last-child {
  border-bottom: 0;
}

.panel-heading + .list-group .list-group-item:first-child {
  border-top-width: 0;
}

.panel > .table {
  margin-bottom: 0;
}

.panel > .panel-body + .table {
  border-top: 1px solid #dddddd;
}

.panel-heading {
  padding: 10px 15px;
  border-bottom: 1px solid transparent;
  border-top-right-radius: 3px;
  border-top-left-radius: 3px;
}

.panel-title {
  margin-top: 0;
  margin-bottom: 0;
  font-size: 16px;
}

.panel-title > a {
  color: inherit;
}

.panel-footer {
  padding: 10px 15px;
  background-color: #f5f5f5;
  border-top: 1px solid #dddddd;
  border-bottom-right-radius: 3px;
  border-bottom-left-radius: 3px;
}

.panel-group .panel {
  margin-bottom: 0;
  overflow: hidden;
  border-radius: 4px;
}

.panel-group .panel + .panel {
  margin-top: 5px;
}

.panel-group .panel-heading {
  border-bottom: 0;
}

.panel-group .panel-heading + .panel-collapse .panel-body {
  border-top: 1px solid #dddddd;
}

.panel-group .panel-footer {
  border-top: 0;
}

.panel-group .panel-footer + .panel-collapse .panel-body {
  border-bottom: 1px solid #dddddd;
}

.panel-default {
  border-color: #dddddd;
}

.panel-default > .panel-heading {
  color: #333333;
  background-color: #f5f5f5;
  border-color: #dddddd;
}

.panel-default > .panel-heading + .panel-collapse .panel-body {
  border-top-color: #dddddd;
}

.panel-default > .panel-footer + .panel-collapse .panel-body {
  border-bottom-color: #dddddd;
}

.panel-primary {
  border-color: #428bca;
}

.panel-primary > .panel-heading {
  color: #ffffff;
  background-color: #428bca;
  border-color: #428bca;
}

.panel-primary > .panel-heading + .panel-collapse .panel-body {
  border-top-color: #428bca;
}

.panel-primary > .panel-footer + .panel-collapse .panel-body {
  border-bottom-color: #428bca;
}

.panel-success {
  border-color: #d6e9c6;
}

.panel-success > .panel-heading {
  color: #468847;
  background-color: #dff0d8;
  border-color: #d6e9c6;
}

.panel-success > .panel-heading + .panel-collapse .panel-body {
  border-top-color: #d6e9c6;
}

.panel-success > .panel-footer + .panel-collapse .panel-body {
  border-bottom-color: #d6e9c6;
}

.panel-warning {
  border-color: #fbeed5;
}

.panel-warning > .panel-heading {
  color: #c09853;
  background-color: #fcf8e3;
  border-color: #fbeed5;
}

.panel-warning > .panel-heading + .panel-collapse .panel-body {
  border-top-color: #fbeed5;
}

.panel-warning > .panel-footer + .panel-collapse .panel-body {
  border-bottom-color: #fbeed5;
}

.panel-danger {
  border-color: #eed3d7;
}

.panel-danger > .panel-heading {
  color: #b94a48;
  background-color: #f2dede;
  border-color: #eed3d7;
}

.panel-danger > .panel-heading + .panel-collapse .panel-body {
  border-top-color: #eed3d7;
}

.panel-danger > .panel-footer + .panel-collapse .panel-body {
  border-bottom-color: #eed3d7;
}

.panel-info {
  border-color: #bce8f1;
}

.panel-info > .panel-heading {
  color: #3a87ad;
  background-color: #d9edf7;
  border-color: #bce8f1;
}

.panel-info > .panel-heading + .panel-collapse .panel-body {
  border-top-color: #bce8f1;
}

.panel-info > .panel-footer + .panel-collapse .panel-body {
  border-bottom-color: #bce8f1;
}

}

    </style>
    <link href="http://twitter.github.com/bootstrap/assets/css/bootstrap-responsive.css" rel="stylesheet">

    <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

    <!-- Fav and touch icons -->
  

	<link rel="apple-touch-icon-precomposed" sizes="144x144" href="http://www.harvix.com/images/harvixshort2.jpg">
    <link rel="apple-touch-icon-precomposed" sizes="114x114" href="http://www.harvix.com/images/harvixshort2.jpg">
      <link rel="apple-touch-icon-precomposed" sizes="72x72" href="http://www.harvix.com/images/harvixshort2.jpg">
                    <link rel="apple-touch-icon-precomposed" href="http://www.harvix.com/images/harvixshort2.jpg">
                                   <link rel="shortcut icon" href="http://www.harvix.com/images/harvixshort2.jpg">

<style>

a:link {text-decoration:none; color:blue;}      /* unvisited link */
a:visited {text-decoration:none; color:blue;}  /* visited link */
a:hover {text-decoration:none; color:blue;}  /* mouse over link */
a:active {text-decoration:none; color:blue;}  /* selected link */

   /* MARKETING CONTENT
    -------------------------------------------------- */

    /* Center align the text within the three columns below the carousel */
    .marketing .span4 {
      text-align: center;
    }
    .marketing h2 {
      font-weight: normal;
    }
    .marketing .span4 p {
      margin-left: 10px;
      margin-right: 10px;
    }


    /* Featurettes
    ------------------------- */

    .featurette-divider {
      margin: 40px 0; /* Space out the Bootstrap <hr> more */
    }
    .featurette {
      overflow: hidden; /* Vertically center images part 2: clear their floats. */
    }

    /* Give some space on the sides of the floated elements so text doesn't run right into it. */
    .featurette-image.pull-left {
      margin-right: 40px;
    }
    .featurette-image.pull-right {
      margin-left: 40px;
    }

    /* Thin out the marketing headings */
    .featurette-heading {
      font-size: 40px;
      font-weight: 300;
      line-height: 1;
      letter-spacing: -1px;
    }
</style>



<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-30447587-1']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>



<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-30658262-1']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>


</head>

  <body>



    <div class="navbar navbar-inverse navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container-fluid">
          <a class="brand" href="index.php"><b><span style="color:white">Har<span style="color:red">vix</span></span></b></a>
            <ul class="nav">
              <li><form class="navbar-search pull-left">
  <input type="text" style="width:650px;" action="http://harvix.com/search3.cgi" onsubmit="submitted('h'); return false" name="q"  class="search-query" value="$query">
</li></ul><ul class="nav"><li>
<button type="submit" class="btn"><strong>Search</strong></button>
</form></li>
</ul>
            </ul>
            </ul>
        </div>
      </div>
    </div>


  <!-- Marketing messaging and featurettes
    ================================================== -->
    <!-- Wrap the rest of the page in another container to center all the content. -->

    <div class="container-fluid">



      <!-- START THE FEATURETTES -->


EOF
;
}

sub print_footer
{
print <<EOX

<!-- /END THE FEATURETTES -->



    </div><!-- /.container -->

  <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="http://harvix.com/assets/jquery.js"></script>
    <script src="http://getbootstrap.com/2.3.2/assets/js/bootstrap-transition.js"></script>
    <script src="http://harvix.com/assets/tab.js"></script>

<script>
    //doesn't block the load event
        function createIframe(){
                var i = document.createElement("iframe");
                var a = Math.random() + "";
                var t = a * 10000000000000;
                i.src = "https://draftin.com/draft/users/sign_in";
                i.scrolling = "auto";
                i.frameborder = "0";
                i.width = "100%";
                i.height = "600px";
                i.style = "border: none";
                document.getElementById("frame4").appendChild(i);
        };
        
        // Check for browser support of event handling capability
        if (window.addEventListener)
        window.addEventListener("load", createIframe, false);
        else if (window.attachEvent)
        window.attachEvent("onload", createIframe);
        else window.onload = createIframe; 
</script>

<script type="text/javascript">
  var vglnk = { api_url: '//api.viglink.com/api',
                key: '5c151b7134e33042b59e84458cd2ca2c' };

  (function(d, t) {
    var s = d.createElement(t); s.type = 'text/javascript'; s.async = true;
    s.src = ('https:' == document.location.protocol ? vglnk.api_url :
             '//cdn.viglink.com/api') + '/vglnk.js';
    var r = d.getElementsByTagName(t)[0]; r.parentNode.insertBefore(s, r);
  }(document, 'script'));
</script>

  </body>
</html>



EOX
;
}


sub parse_query
{
        my $query = $ENV{QUERY_STRING} || shift || 1;

        $query =~ s/q=//;
        $query = urldecode($query);
        #$query =~ s/\+/ /g;
        $query =~ s/[\[\]\(\)\.\?]/ /g;
        $query =~ s/^\s*//;
        $query =~ s/\s*$//;
        $query =~ s/\s+/ /g;

        return $query;
}

