%for value in movie.itervalues():
 <p>{{value}}</p>
%end
%for ca in coactor:
 <p>{{ca}}</p>
%end

%rebase layout
