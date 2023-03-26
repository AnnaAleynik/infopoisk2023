class SearchesController < ApplicationController
  def show
    @search_data = sorted_search_data
  end

  helper_method :link_by_file_name

  private

  def sorted_search_data
    search_data
      .sort_by { |item| -item[1] }
      .select { |item| item[1] != 0 }
  rescue
  end

  def search_data
    stdout, stdeerr, status = Open3.capture3("python3 search.py \"#{search_term}\"")
    JSON.parse stdout
  end

  def search_term
    params[:search].downcase || ""
  end

  def link_by_file_name(file_name)
    # binding.pry
    file_name = file_name.split("-").last.split(".").first

    index_data.select { |i| i[1].split("/").last.split(".").first == file_name }.first&.first
  end

  def index_data
    @index_data ||= File.open("index.txt").read.split("\n").map {|i| i.split(",")}
  end
end
